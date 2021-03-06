import flask
import git
import socket
import redis

api = flask.Flask(__name__)
cache = redis.Redis(host='redis-lb', port=6379)

@api.route('/')
def hello():
    return flask.redirect('/info')

@api.route('/counter', methods=['GET'])
def get_counter():
  count = cache.incr('count')
  return "<h1> Hi, Welcome to counter</h1> <br/> Counter value in GET Request: {}".format(count)

@api.route('/counter', methods=['POST'])
def add_counter():
  count = cache.incrby('count', 2)
  return "<h1> Hi, Welcome to counter</h1> <br/> Counter value in POST Request: {}".format(count),200

@api.route('/counter', methods=['DELETE'])
def delete_counter():
  count = cache.decr('count')
  return "<h1> Hi, Welcome to counter</h1> <br/> Counter value in DELETE Request: {}".format(count),200

@api.route('/info', methods=['GET'])
def get_info():
  repo = git.Repo(search_parent_directories=True)
  sha = repo.head.object.hexsha
  branch = repo.active_branch
  hostname = socket.gethostname()
  return "<h1> Hi, Welcome to info </h1>Latest commit hash : {0} <br/> Active branch : {1} <br/> Hostname/ContainerID : {2}".format(sha, branch, hostname)




if __name__ == '__main__':
    api.run(host="0.0.0.0", debug=True)
