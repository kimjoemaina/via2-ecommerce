<p align="center"><img src="https://via2-ecommerce.s3.amazonaws.com/images/logo.png" width="auto" height="auto"></p>
<h3 align="center">Via2-Ecommerce Django Application</h3>
<p align="center"><a href="https://via2-ecommerce.herokuapp.com/">Via2 Ecommerce (Heroku)</a></p>

<p align="center">
  <a href="#-prerequisites">Prerequisites</a> · <a href="#-introduction">Introduction</a> · <a href="#-Demo">Demo</a> · 
  <a href="#-contributing">Contributing</a> · <a href="#-faq">FAQ</a> · 
  <a href="#-donate">Donate</a>
</p>

## Prerequisites

To run the application in your environment, you need:
- Django `pip install django`
- Requests `pip install requests`
- Pillow `pip install pillow`
- Boto3 `pip install boto3`

## 🤝 Introduction

Via2 is wordplay on the swahili word 'viatu' which means shoes. The web app employs Django as the back-end and HTML, CSS, JS for the front-end.

The DB used in Postgres. However, you can use any database of your choice. Ensure to enter your credentials in the settings file and to update your environemt variables.

NB: The PayPal checkout is currently a development sandbox. Customize this to your own sandbox for testing. Also note that on checkout the grand total (KES) is converted to USD.

Features:

- Adding, updating, deleting products and their variations.
- Product categories.
- Paginator. (Currenty set to 3 products per page on the [Store](https://via2-ecommerce.herokuapp.com/store/) page )
- Adding multiple variations to cart.
- Checkout (PayPal, Debit/Credit card supported)
- User registration and login forms.
- User profile update.
- Search functionality.

## 🧪 Demo

The demo can be accessed [here](https://via2-ecommerce.herokuapp.com/store/).

Ensure that you get rid of all development parameters before deploying to production.

## 📢 Contributing

If you'd like to contribute, feel free to open a [pull request](https://github.com/kimjoemaina/POS/pulls) and we can collaborate!

## 🫙 Donate

Buy me a coffee to help me keep going! ☕

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=XVNG6ATBXFJAC)\



