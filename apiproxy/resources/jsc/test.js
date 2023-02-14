var proxyName = context.getVariable("apiproxy.name");
var tenantPrefix = proxyName.split("-",1);
context.setVariable("properties.tenant-prefix", tenantPrefix[0]);


 var obj =  {
	"index": context.getVariable("private.tenant.splunk.index"),
	"event": {
// 		"log-type": "Apigee proxy logs for " + context.getVariable("properties.tenant-prefix"),
// 		"org": context.getVariable("organization.name"),
// 		"environment": context.getVariable("environment.name"),
// 		"developer-email": context.getVariable("apigee.developer.email"),
// 		"developer-id": context.getVariable("apigee.developer.id"),
// 		"developer-app-name": context.getVariable("apigee.developer.app.name"),
// 		"developer-app-id":context.getVariable("developer.app.id"),
// 		"api-product-name": context.getVariable("apiproduct.name"),
// 		"api-proxy-name": context.getVariable("apiproxy.name"),
// 		"api-proxy-revision": context.getVariable("apiproxy.revision"),
// 		"request-header-XForwarded-For": context.getVariable("request.header.X-Forwarded-For"),
// 		"developer-app-id": context.getVariable("developer.app.id"),
// 		"target-url": context.getVariable("target.url"),
// 		"client-IP": context.getVariable("proxy.client.ip"),
// 		"message-status-code": context.getVariable("message.status.code"),
// 		"proxy-basepath": context.getVariable("proxy.basepath"),
// 		"proxy-pathsuffix": context.getVariable("proxy.pathsuffix"),
// 		"proxy-url": context.getVariable("proxy.url"),
// 		"message-id": context.getVariable("messageid"),
// 		"error": context.getVariable("error"),
// 		"error-status-code": context.getVariable("error.status.code"),
// 		"error-message": context.getVariable("error.message"),
// 		"error-reason-phrase": context.getVariable("error.reason.phrase"),
// 		"error-state": context.getVariable("error.state"),
// 		"response-reason-phrase": context.getVariable("message.reason.phrase"),
// 		"virtualhost-name": context.getVariable("virtualhost.name"),
// 		"request-header-host": context.getVariable("request.header.host"),
// 		"fault-name": context.getVariable("fault.name"),
// 		"request-uri": context.getVariable("request.uri"),
// 		"request-verb": context.getVariable("request.verb"),
// 		"response-content-length": context.getVariable("response.header.Content-Length"),
// 		"response-status-code": context.getVariable("response.status.code"),
		
		"request-received-time": context.getVariable("client.received.start.time"),
		"request-received-timestamp": context.getVariable("client.received.start.timestamp"),
		"request-received-end-timestamp": context.getVariable("client.received.end.timestamp"),
		"response-sent-time": context.getVariable("client.sent.end.time"),
        "response-sent-timestamp": context.getVariable("client.sent.end.timestamp"),
		"request-received-time": context.getVariable("target.received.start.time"),
		"target-received-end-time": context.getVariable("target.received.end.time"),
		
		"client-received-start-time": context.getVariable("client.received.start.time"),
		"target-received-end-time": context.getVariable("target.received.end.time"),
		
		"client-received-start-timestamp": context.getVariable("client.received.start.timestamp"),
		"target-received-end-timestamp": context.getVariable("target.received.end.timestamp"),
		
		"time1": context.getVariable("target.received.end.timestamp") - context.getVariable("client.received.start.timestamp"),
		"time2": context.getVariable("target.received.end.timestamp") - context.getVariable("response.received.start.timestamp")
		// "msg-start-UTC-time": {timeFormatMs("yyyy-MM-dd HH-mm-ss.SSS",client.received.start.timestamp)},
		// "msg-end-UTC-time": {timeFormatMs("yyyy-MM-dd HH-mm-ss.SSS",client.sent.end.timestamp)}
	  },
	"sourcetype": "json"
};

// var receiveStream = context.getVariable("response.transport.message").GetResponseStream();
// var readStream = new StreamReader (receiveStream, Encoding.UTF8);
// var text = readStream.ReadToEnd();

// print(text);
// print(context.getVariable("target.received.end.time"));
print(JSON.stringify(obj));

print(context.getVariable("target.received.end.timestamp") - context.getVariable("client.received.start.timestamp"));



