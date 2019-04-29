import requests
from bs4 import BeautifulSoup
import config
from RentalObject import RentalObject
from dao import write_dao, base


def parse_main_page(str):
    if str == "bostad":
        session_requests = requests.session()
        response = session_requests.get(config.BU_LOGIN_URL)
        soup = BeautifulSoup(response.text, features="lxml")
        for n in soup('input'):
            if n['name'] == '__RequestVerificationToken':
                authenticity_token = n['value']
                break
        print(authenticity_token)
        payload = {
            "LoginDetails.PersonalIdentityNumberOrEmail": config.USERNAME,
            "LoginDetails.Password": config.PASSWORD,
            "__RequestVerificationToken": authenticity_token
        }
        response = session_requests.post(
            config.BU_LOGIN_URL,
            data=payload,
            headers=dict(referer=config.BU_LOGIN_URL)
        )
        print(response)
        response = session_requests.get(
            config.BU_URL,
            headers=dict(referer=config.BU_LOGIN_URL)
        )
        soup = BeautifulSoup(response.text, features="lxml")
        results = soup.find_all("div", "rentalobject")
        rentals = []
        for result in results:
            rental = RentalObject(result)
            write_dao.save_object(rental.get_insert_list())
        base.write_commit()
        base.close_connection()
        '''
        for span in spans.items():
            print(span)
        print(len(spans))
        '''

    elif str == "nationsgardarna":
        raise NotImplementedError
