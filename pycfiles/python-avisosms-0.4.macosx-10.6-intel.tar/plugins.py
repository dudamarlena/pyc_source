# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/avisosms/plugins.py
# Compiled at: 2014-01-30 04:26:18
import hashlib

class AvisoSMSPlugin(object):
    pass


class SendSMSPlugin(AvisoSMSPlugin):

    def send_sms(self, source_phone, dest_phone, message):
        data = {'username': self.username, 
           'password': self.password, 
           'send_message': [
                          {'destination_address': dest_phone, 
                             'message': message, 
                             'source_address': source_phone}]}
        return self.post_json(url='/sms/json/1/', data=data)

    def get_sms_state(self, message_ids):
        if not isinstance(message_ids, (list, tuple)):
            message_ids = [
             message_ids]
        data = {'get_message_state': message_ids, 
           'username': self.username, 
           'password': self.password}
        return self.post_json(url='/sms/json/1/', data=data)


class BalancePlugin(AvisoSMSPlugin):

    def get_balance(self):
        data = {'get_billing_balance': [], 'username': self.username, 
           'password': self.password}
        return self.post_json(url='/sms/json/1/', data=data)


class MobileCommercePlugin(AvisoSMSPlugin):
    mc_statuses_dict = {0: 'Нет ошибок. Операция произведена успешно.', 
       1: 'Неожиданная ошибка. Этой ошибки быть не должно.', 
       2: 'Эта ошибка может возникнуть, если для данного номера не доступна услуга мобильной коммерции.', 
       3: 'Некоторые параметры переданы неверно или не переданы.', 
       4: 'Ошибка авторизации.', 
       5: 'Ошибка проверки цифровой подписи.', 
       6: 'Слишком частая инициация платежа на данный номер (Только для МТС).'}

    def get_sign(self, phone):
        if all([self.service_id, self.secure_hash]):
            hash = hashlib.md5()
            hash.update(phone)
            hash.update(str(self.service_id))
            hash.update(self.username)
            hash.update(self.secure_hash)
            return hash.hexdigest()
        raise Exception('You should provide service_id and secure_hash')

    def create_order(self, phone, price, description, order_id=None, success_message=None, test=True):
        if len(description) < 11:
            raise Exception('Description should be at least 10 symbols long')
        data = {'username': self.username, 'sign': self.get_sign(phone), 
           'description': description, 
           'price': price, 
           'service_id': self.service_id, 
           'success_message': success_message, 
           'phone': phone, 
           'merchant_order_id': order_id, 
           'test': test}
        return self.post_json(url='/mc/create_order/', data=data)

    def get_order_status(self, phone, order_id):
        data = {'username': self.username, 
           'sign': self.get_sign(phone), 
           'service_id': self.service_id, 
           'order_id': order_id}
        return self.post_json(url='/mc/get_order_info/', data=data)


class TelephoneBookPlugin(AvisoSMSPlugin):

    def create_telephone_book_record(self, name, phone, comment, access_key=None):
        data = {'user': self.username, 
           'response_type': 'json', 
           'request_type': 'add', 
           'name': name, 
           'number': phone, 
           'comment': comment, 
           'access_key': access_key}
        return self.post_json(url='/telephone_book/', data=data)

    def update_telephone_book_record(self, id, name, phone, comment, access_key=None):
        data = {'user': self.username, 
           'response_type': 'json', 
           'request_type': 'edit', 
           'id': id, 
           'name': name, 
           'number': phone, 
           'comment': comment, 
           'access_key': access_key}
        return self.post_json(url='/telephone_book/', data=data)

    def delete_telephone_book_record(self, id, access_key):
        data = {'user': self.username, 
           'response_type': 'json', 
           'request_type': 'delete', 
           'id': id, 
           'access_key': access_key}
        return self.post_json(url='/telephone_book/', data=data)

    def list_telephone_book_records(self, access_key):
        data = {'user': self.username, 
           'response_type': 'json', 
           'request_type': 'list', 
           'access_key': access_key}
        return self.post_json(url='/telephone_book/', data=data)

    def search_telephone_book_record(self, query, access_key):
        data = {'user': self.username, 
           'response_type': 'json', 
           'request_type': 'search', 
           'search': query, 
           'access_key': access_key}
        return self.post_json(url='/telephone_book/', data=data)


class CheckPrefixPlugin(AvisoSMSPlugin):

    def check_prefix(self, prefix):
        data = {'prefix': prefix}
        return self.post_json(url='/whois', data=data)


class RARPlugin(AvisoSMSPlugin):

    def create_referal_user(self, ref_username, ref_password, email, phone, referral_id):
        data = {'username': ref_username, 
           'password': ref_password, 
           'email': email, 
           'phone': phone, 
           'referral': referral_id}
        return self.post_json(url='/rar/', data=data)