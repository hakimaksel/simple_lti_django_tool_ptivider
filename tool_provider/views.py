from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template import Context

from ims_lti_py.tool_provider import DjangoToolProvider

from utils import oauth_creds

@csrf_exempt
def lti_tool(request):
	key = request.POST['oauth_consumer_key']
	if key:
		secret = oauth_creds[key]
		if secret:
			tp = DjangoToolProvider(key, secret, request.POST)
		else:
			tp = DjangoToolProvider(None, None, request.POST)
			tp.lti_msg = "Your consumer didn't used a recognized key"
			tp.lti_errorlog = "You did it wrong!"
			error_temp = get_template("error.html")
			context_data = Context({'message': 'Consumer key not recognized', 
				'params': request.POST})
			error_html = error_temp.render(context_data)
			return HttpResponse(error_html)	

	else:
		key_error_temp = get_template("error.html")
		key_error_html = key_error_temp.render(Context({'message': 'Consumer key not recognized'}))
		return HttpResponse(key_error_html)

	if not tp.is_valid_request(request):
		sigerror_temp = get_template("error.html")
		context_data = Context({'message': 'The OAuth signature is invalid', 
				'params': request.POST})
		sigerror_html = sigerror_temp.render(context_data)		
		return HttpResponse(sigerror_html)


	request.session['launch_params'] = tp.to_params()
	userid = request.POST['user_id']
	temp = get_template('boring_tool.html')
	html = temp.render(Context({'userid': userid}))
	return HttpResponse(html)

@csrf_exempt
def assessment(request):
	if request.session['launch_params']:
		key = request.session['launch_params']['oauth_consumer_key']
		secret = oauth_creds[key]
	else:
		key_error_temp = get_template("error.html")
		key_error_html = key_error_temp.render(Context({'message': 'The tool never launched'}))
		return HttpResponse(key_error_html)

	tp = DjangoToolProvider(key, secret, request.session['launch_params'])

	score = request.POST['score']
	tp.post_replace_result(resp)
	temp = get_template('assessment_finished.html')
	html = temp.render(Context({'score': score}))
	return HttpResponse(html)
