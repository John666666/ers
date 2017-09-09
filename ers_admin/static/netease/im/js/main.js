/**
 * 主要业务逻辑相关
 */
setCookie('uid','18668938752');
		//自己的appkey就不用加密了
		// setCookie('sdktoken',pwd);
setCookie('sdktoken','741b497aecce23ccdedc81d6b645a1ca');
var userUID = readCookie("uid")
/**
 * 实例化
 * @see module/base/js
 */
var yunXin = new YX(userUID)
yunXin.openChatBox('356521041000146',"p2p");
yunXin.myNetcall.onClickNetcallLink(Netcall.NETCALL_TYPE_AUDIO);



