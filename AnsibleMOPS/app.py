from flask import Flask, Response, request, jsonify
import subprocess
import shlex
import signal
from datetime import datetime

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException()

signal.signal(signal.SIGALRM, handler)

app = Flask(__name__)

def extract_failed_and_ignored_counts(output):
    lines = output.strip().split('\n')[-10:]
    
    ok_count = failed_count = ignored_count = 0
    
    for line in lines:
        if "failed=" in line:
            failed_count = int(line.split("failed=")[1].split()[0])
        if "ignored=" in line:
            ignored_count = int(line.split("ignored=")[1].split()[0])
        if "ok=" in line:
            ok_count = int(line.split("ok=")[1].split()[0])
    return ok_count, failed_count, ignored_count

def run_playbook(command_line):
    command = shlex.split(command_line)
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        signal.alarm(120)

        stdout, _ = process.communicate()
        signal.alarm(0)

        ok_count, failed_count, ignored_count = extract_failed_and_ignored_counts(stdout.decode())
        print("playbookResource output:")
        for line in stdout.decode().splitlines():
            print(line)
        if process.returncode == 0 and failed_count == 0:
            return jsonify({
                "status": "Success",
                "timeStamp": timestamp,
                "okCount": ok_count,
                "playbookResource": stdout.decode()
            }), 200
        else:
            return jsonify({
                "status": "Failed",
                "errorMsg": "Playbook execution resulted in failures or ignores",
                "timeStamp": timestamp,
                "playbookResource": stdout.decode()
            }), 500
        

    except TimeoutException:
        return Response("[{}] Timeout: No response from nodes in 120 seconds".format(timestamp), status=408, content_type='text/plain')
    except Exception as e:
        return jsonify({
            "status": "Failed",
            "errorMsg": str(e),
            "timeStamp": timestamp
        }), 500

@app.route('/run_session_down', methods=['POST'])
def run_session_down():
    required_fields = ["nodeName", "neighbour", "context", "additionalText"]
    data = request.json or {}
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response("Missing fields: {}".format(', '.join(missing_fields)), status=400)

    command_line = "ansible-playbook -i localhost, -c local -e 'node_name={} context_={} additionalText={} neighbour={}' ./MOP1BFDSessionDown/MOP1fullContext.yml".format(data['nodeName'], data['context'], data['additionalText'], data['neighbour'])
    return run_playbook(command_line)

@app.route('/run_card_missing', methods=['POST'])
def run_card_missing():
    required_fields = ["nodeName", "additionalText", "cardNumber"]
    data = request.json or {}
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response("Missing fields: {}".format(', '.join(missing_fields)), status=400)

    command_line = "ansible-playbook -i localhost, -c local -e 'nodeName={} additionalText={} cardNumber={}' ./MOP2CardMissing/MOP2.yml --extra-vars 'confirm_reload=Y'".format(data['nodeName'], data['additionalText'], data['cardNumber'])
    return run_playbook(command_line)


@app.route('/run_switch_down', methods=['POST'])
def run_switch_down():
    required_fields = ["deviceIP", "enmpIP", "ndRef"]
    data = request.json or {}
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response("Missing fields: {}".format(', '.join(missing_fields)), status=400)
    command_line = (
        "ansible-playbook -i localhost, -c local -e 'deviceIP={} enmpIP={} ndRef={}' ./MOP3SWTDOWN/MOP3SWTDOWN.yml".format(data['deviceIP'], data['enmpIP'], data['ndRef'])
    )
    return run_playbook(command_line)



if __name__ == '__main__':
    app.run(port=5022, debug=False)  # Turn off debug for production
