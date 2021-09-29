import grpc

from user_srv.proto import user_pb2, user_pb2_grpc


class UserTest:
    def __init__(self):
        # 连接grpc
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=2))
        print("total:", rsp.total)
        for user in rsp.data:
            print(user.mobile, user.birthday)

    def get_user_by_id(self, id):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(id=id))
        print(rsp.mobile)

    def get_user_by_mobile(self, mobile):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserByMobile(user_pb2.Mobile(mobile=mobile))
        print(rsp.id, rsp.mobile)

    def create_user(self, nick_name, mobile, password):
        rsp: user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            nickName=nick_name,
            mobile=mobile,
            password=password
        ))

        print(rsp.id)

    def update_user(self, id, nick_name, gender, birthday):
        self.stub.UpdateUser(user_pb2.UpdateUserInfo(
            id=id,
            nickName=nick_name,
            gender=gender,
            birthday=birthday
        ))


if __name__ == '__main__':
    user = UserTest()
    # user.user_list()
    # user.get_user_by_id(1)
    # user.get_user_by_id(2)
    # user.get_user_by_id(3)
    # user.get_user_by_id(4)
    # user.get_user_by_id(20)
    # user.get_user_by_mobile("1878222223")

    # user.create_user("yuanyuan", "18000770603", "hahaha")

    user.update_user(11, "love_yuan", "女", 1111111111)