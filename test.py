import unittest

import requests


class ApiTest(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"


    USER_URL =URL + "users"
    USER_post_data = {'firstName': "batman" , "lastName": "Robin"}
    USER_put_data = {'firstName': "change_firstname" }



    Email_URL = URL + "Email"
    EMAIL_post_data = {"email": "himadu@vit.conm", "user_id": 1 }
    EMAIL_put_data = {"email": "change@email.id"}



    Number_URL = URL +"PhoneNumber"
    Number_Post_data = {"number": "123654", "user_id": 1}
    Number_Put_data = {"number": "6554455"}


 
    def test_1_post_USER(self):
        response = requests.post(ApiTest.USER_URL , data= ApiTest.USER_post_data)
        self.assertEqual(response.status_code, 201)
        
        
    def test_2_get_all_users(self):
        response = requests.get(ApiTest.USER_URL)
        self.assertEqual(response.status_code , 200)
        
    
    def test_3_get_USER1(self):

        response = requests.get(ApiTest.USER_URL +"/1")
        self.assertEqual(response.status_code, 200)
            

    def test_4_PUT_User1(self):
        response = requests.put(ApiTest.USER_URL +"/1", data= ApiTest.USER_put_data)
        

        self.assertEqual(response.status_code , 204)
    


    def test_5_post_Email(self):
        response = requests.post(ApiTest.Email_URL , data= ApiTest.EMAIL_post_data)
        self.assertEqual(response.status_code, 201)
        
    def test_6_get_all_Email(self):
        response = requests.get(ApiTest.Email_URL)
        self.assertEqual(response.status_code , 200)
        
        
    
    def test_7_get_Email1(self):
        response = requests.get(ApiTest.Email_URL +"/1")
        self.assertEqual(response.status_code, 200)
            

    def test_8_PUT_Email1(self):
        response = requests.put(ApiTest.Email_URL +"/1", data= ApiTest.EMAIL_put_data)

        self.assertEqual(response.status_code , 204)
        

    def test_9_post_Number(self):

        response = requests.post(ApiTest.Number_URL , data= ApiTest.Number_Post_data)
        
        self.assertEqual(response.status_code, 201)
    
        
    def test_10_get_all_Number(self):
        response = requests.get(ApiTest.Number_URL)
        self.assertEqual(response.status_code , 200)
        
    def test_11_get_Number1(self):


        response = requests.get(ApiTest.Number_URL +"/1")
        
        self.assertEqual(response.status_code, 200)

    def test_12_PUT_Number1(self):

        response  = requests.put(ApiTest.Number_URL +"/1", data =ApiTest.Number_Put_data )
        self.assertEqual(response.status_code , 204)
        
       

    
    


if __name__ == '__main__':
    
    
    unittest.main()