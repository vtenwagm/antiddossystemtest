from flask import Flask, request, abort,render_template
from datetime import datetime, timedelta

app = Flask(__name__)

black_list = []
ip_request_count = {}
REQUEST_LIMIT = 2
	

@app.errorhandler(502)
def page_not_found(e):
	return render_template('502.html'), 502

@app.before_request
def before_request():
	if request.access_route[0] in black_list:
		return abort(502)
	# Lấy địa chỉ IP của người dùng
	ip_address = request.access_route[0]
	
	# Kiểm tra xem IP đã được lưu trong dictionary chưa
	if ip_address in ip_request_count:
		# Nếu đã tồn tại, kiểm tra thời điểm cuối cùng request
		last_request_time = ip_request_count[ip_address]['time']
		current_time = datetime.now()
	
		# Tính khoảng thời gian giữa hai request
		time_difference = current_time - last_request_time
	
		# Nếu khoảng thời gian nhỏ hơn 1 giây và số lượng request vượt quá giới hạn, trả về thông báo lỗi
		if time_difference < timedelta(seconds=1) and ip_request_count[ip_address]['count'] >= REQUEST_LIMIT:
			black_list.append(ip_address)
			abort(502)
	
		# Nếu khoảng thời gian lớn hơn 1 giây, đặt lại số lượng request và thời điểm cuối cùng
		elif time_difference >= timedelta(seconds=1):
			ip_request_count[ip_address] = {'count': 1, 'time': current_time}
		else:
			# Nếu khoảng thời gian nhỏ hơn 1 giây và số lượng request không vượt quá giới hạn, tăng số lượng request
			ip_request_count[ip_address]['count'] += 1
	else:
		# Nếu IP chưa được lưu, thêm nó vào dictionary
		ip_request_count[ip_address] = {'count': 1, 'time': datetime.now()}
	

@app.route('/')
def home():
	return 'test anti_ddos sẻvice'

if __name__ == '__main__':
	try:
		app.run(host='0.0.0.0',port=8080)
	except (e) :
		with open("error.log",'w') as f : f.write(e)
