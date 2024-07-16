
from django.utils.deprecation import MiddlewareMixin
from mobileesp import mdetect

class MobileDetectionMiddleware(MiddlewareMixin
                                ):
    def process_request(self, request):
        is_mobile = False

        user_agent = request.META.get("HTTP_USER_AGENT")
        http_accept = request.META.get("HTTP_ACCEPT")
        if user_agent and http_accept:
            agent = mdetect.UAgentInfo(userAgent=user_agent, httpAccept=http_accept)
            is_tablet = agent.detectTierTablet()
            is_phone = agent.detectTierIphone()
            is_mobile = is_tablet or is_phone or agent.detectMobileQuick()

        request.is_mobile = is_mobile
