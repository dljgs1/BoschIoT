# 服务中心 提供对服务请求和反馈的中转
# 目前只支持单服务独占 不支持服务多路复用

from gevent import monkey
from gevent.pywsgi import WSGIServer, WSGIHandler

monkey.patch_all()
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import threading
import asyncio
import time

# 任务池
task_pool = {}  # 当前的任务数据
idle_pool = {}  # 当前服务是否可用
service_machine = {'MNIST': 'MNIST'}

lock = threading.Lock()


# 同步
@app.route('/sync', methods=["POST"])
def sync():
    tp = request.form['type']
    data = request.form['data']
    idle = request.form['id']  # 会话session
    if tp == 'sync':  # 同步心跳
        idle_pool[idle] = True  # 当前服务可用
        if not idle_pool[idle]:  # 有人使用了服务 传输服务类型与数据
            print("task_pool[sess]:", task_pool[idle])
            return jsonify({"type": task_pool[idle]['type'], "data": task_pool[idle]['data'], "token": str(1223)})
        else:
            return jsonify({"alert": "no task"})
    elif tp == 'ret':  # 返回结果
        print("get answer")
        # lock.acquire()
        task_pool[idle] = data
        idle_pool[idle] = True  # 重新进入空闲
        # lock.release()
        return jsonify({"type": "ok"})
    return jsonify({"alert": "none type"})


# 上传数据 请求服务
@app.route('/reqserv', methods=["POST"])
def reqest_service():
    print("reqserv!!!")
    serv = request.form['service']
    data = request.form['data']
    idle = None
    print("req lock")
    # lock.acquire()  # 占用当前可用机器
    for i in idle_pool:
        if idle_pool[i]:
            idle_pool[i] = False
            task_pool[i] = {'data': data, 'type': serv}
            idle = i
            break
    if idle is None:
        return "no such service"
    # lock.release()
    print("lock release process...")
    while not idle_pool[idle]:  # 等待处理结束
        time.sleep(0.5)

    return jsonify(task_pool[idle])


@app.route('/')
def index():
    return "/reqserv： 上传数据<br> /sync 同步心跳"


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=1060, threaded=True)
    http_server = WSGIServer(('0.0.0.0', 1058), app)
    http_server.serve_forever()
