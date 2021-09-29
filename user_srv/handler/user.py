import time, datetime

import grpc
from loguru import logger
from passlib.hash import pbkdf2_sha256
from google.protobuf import empty_pb2

from user_srv.model.models import User
from user_srv.proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):

    @staticmethod
    def convert_user_to_rsp(user):
        user_info_rsp = user_pb2.UserInfoResponse()

        user_info_rsp.id = user.id
        user_info_rsp.password = user.password
        user_info_rsp.mobile = user.mobile
        user_info_rsp.role = user.role

        if user.nick_name:
            user_info_rsp.nickName = user.nick_name

        if user.gender:
            user_info_rsp.gender = user.gender

        if user.birthday:
            user_info_rsp.birthday = int(time.mktime(user.birthday.timetuple()))

        return user_info_rsp

    @logger.catch()
    def GetUserList(self, request: user_pb2.PageInfo, context):
        """
        获取用户列表
        :param request:
        :param context:
        :return:
        """
        rsp = user_pb2.UserListResponse()
        users = User.select()
        rsp.total = users.count()

        # 分页
        page = 1
        per_page_nums = 10  # 每一页的数量

        if request.pSize:
            per_page_nums = request.pSize

        if request.pn:
            page = request.pn

        start = per_page_nums * (page - 1)

        users = users.limit(per_page_nums).offset(start)

        for user in users:
            rsp.data.append(self.convert_user_to_rsp(user))

        return rsp

    @logger.catch()
    def GetUserById(self, request: user_pb2.IdRequest, context):
        """
        通过id查询用户
        :param request:
        :param context:
        :return:
        """
        try:
            user = User.get(User.id == request.id)

            return self.convert_user_to_rsp(user)

        except User.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch()
    def GetUserByMobile(self, request: user_pb2.Mobile, context):
        """
        通过mobile查询用户
        :param request:
        :param context:
        :return:
        """
        try:
            user = User.get(User.mobile == request.mobile)

            return self.convert_user_to_rsp(user)

        except User.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    @logger.catch()
    def CreateUser(self, request: user_pb2.CreateUserInfo, context):
        """
        新建用户
        :param request:
        :param context:
        :return:
        """
        try:
            user = User.get(User.mobile == request.mobile)

            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("用户已存在")
            return user_pb2.UserInfoResponse()

        except User.DoesNotExist as e:
            pass

        user = User()
        user.nick_name = request.nickName
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.password)
        user.save()

        return self.convert_user_to_rsp(user)

    @logger.catch()
    def UpdateUser(self, request: user_pb2.UpdateUserInfo, context):
        """
        更新用户
        :param request:
        :param context:
        :return:
        """
        try:
            user = User.get(User.id == request.id)

            user.nick_name = request.nickName
            user.gender = request.gender
            user.birthday = datetime.date.fromtimestamp(request.birthday)
            user.save()
            return empty_pb2.Empty()

        except User.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()