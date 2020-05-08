from flask import Flask, url_for, request, render_template, json, redirect, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data import db_session
from data.users import User
from data.news import News
from data.LoginForm import LoginForm
from data.RegisterForm import RegisterForm
from data.NewsForm import NewsForm
from data.AcceptForm import AcceptForm
from data.AdminForm import AdminForm
from data.RedacuserForm import RedacuserForm
from random import choice
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from werkzeug.utils import secure_filename
from os import path
from PIL import Image

chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
spisok_obyazatelnih_symvolov = '(.,:;?!*+%-@[]{}/_$#)'
spisok_vozmojnih_symvolov = chars + spisok_obyazatelnih_symvolov + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
name_symvols = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя" + chars + \
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gamepyed_DUK124EBVBSURNV56LDU71IFGVN'
login_manager = LoginManager()
login_manager.init_app(app)


def len_passw(passw):
    if len(passw) < 8 or len(passw) > 24:
        return 0
    else:
        return 1


def bad_symvols(passw):
    bad_symvol = False
    for i in passw:
        if i not in spisok_vozmojnih_symvolov:
            bad_symvol = True
    if bad_symvol:
        return 0
    else:
        return 1


def registr(passw):
    upper = False
    lower = False
    for i in passw:
        if i.isupper():
            upper = True
        elif i.islower():
            lower = True
    if not upper or not lower:
        return 0
    else:
        return 1


def digit(passw):
    digit = False
    wordd = False
    for i in passw:
        if i.isdigit():
            digit = True
        elif i in "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wordd = True
    if not digit or not wordd:
        return 0
    else:
        return 1


def must_symvols(passw):
    must = False
    wordd = False
    for i in passw:
        if i in spisok_obyazatelnih_symvolov:
            must = True
        elif i in "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wordd = True
    if not must or not wordd:
        return 0
    else:
        return 1


def date():
    Dict_Month = {1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля", 5: "Мая", 6: "Июня",
                  7: "Июля", 8: "Августа", 9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"}
    DATA = datetime.datetime.now()
    DATA2 = " ".join([str(i) for i in
                      [[str(DATA.hour) if len(str(DATA.hour)) == 2 else "0" + str(DATA.hour)][0] +
                       ":" + [str(DATA.minute) if len(str(DATA.minute)) == 2
                              else "0" + str(DATA.minute)][0], DATA.day, Dict_Month[DATA.month],
                       DATA.year, "года"]])
    return DATA2


def mailing(to, kod):
    sender_email = "info.gamepyed@gmail.com"
    receiver_email = to
    password = "gamepyed_Jk2yKV4BtJ6vk@LK"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Добро пожаловать на GAMEPYED!"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""Привет!\nМы рады, что ты теперь с нами!
    Для начала использования нашего сервиса необходимо подтвердить свой аккаунт. Введи код:
    {kod}\nна нашем сайте или перейди по ссылке:\nhttp://127.0.0.1:5000/checkemail/key={kod}\n
    Если у тебя есть какие-либо вопросы, просто ответь на это письмо - мы всегда рады помочь.\n
    С уважением,\nКоманда GAMEPYED"""

    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html style="width:100%;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0;">
    <head>
        <meta content="width=device-width, initial-scale=1" name="viewport">
        <meta charset="UTF-8">
        <meta name="x-apple-disable-message-reformatting">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta content="telephone=no" name="format-detection">
        <title>GAMEPYED</title>
        <!--[if (mso 16)]>
        <style type="text/css">
        a {text-decoration: none;}


        </style>
        <![endif]-->
        <!--[if gte mso 9]>
        <style>sup { font-size: 100% !important; }</style><![endif]-->
        <!--[if !mso]><-- -->
        <link href="https://fonts.googleapis.com/css?family=Lato:400,400i,700,700i" rel="stylesheet">
        <!--<![endif]-->
        <style type="text/css">
    @media only screen and (max-width:600px) {p, ul li, ol li, a { font-size:16px!important; line-height:150%!important } h1 { font-size:30px!important; text-align:center; line-height:120%!important } h2 { font-size:26px!important; text-align:center; line-height:120%!important } h3 { font-size:20px!important; text-align:center; line-height:120%!important } h1 a { font-size:30px!important } h2 a { font-size:26px!important } h3 a { font-size:20px!important } .es-menu td a { font-size:16px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:16px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:16px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:12px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } a.es-button { font-size:20px!important; display:block!important; border-width:15px 25px 15px 25px!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } .es-desk-hidden { display:table-row!important; width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } .es-desk-menu-hidden { display:table-cell!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } }
    #outlook a {
    	padding:0;
    }
    .ExternalClass {
    	width:100%;
    }
    .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {
    	line-height:100%;
    }
    .es-button {
    	mso-style-priority:100!important;
    	text-decoration:none!important;
    }
    a[x-apple-data-detectors] {
    	color:inherit!important;
    	text-decoration:none!important;
    	font-size:inherit!important;
    	font-family:inherit!important;
    	font-weight:inherit!important;
    	line-height:inherit!important;
    }
    .es-desk-hidden {
    	display:none;
    	float:left;
    	overflow:hidden;
    	width:0;
    	max-height:0;
    	line-height:0;
    	mso-hide:all;
    }


        </style>
    </head>
    <body style="width:100%;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0;">
    <div class="es-wrapper-color" style="background-color:#F4F4F4;">
        <!--[if gte mso 9]>
        <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
            <v:fill type="tile"
                    src="https://ifbvig.stripocdn.email/content/guids/CABINET_5127014f192531500fc499f30efa171c/images/34311588845663554.png"
                    color="#f4f4f4" origin="0.5, 0" position="0.5,0"></v:fill>
        </v:background>
        <![endif]-->
        <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
               background="https://ifbvig.stripocdn.email/content/guids/CABINET_5127014f192531500fc499f30efa171c/images/34311588845663554.png"
               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://ifbvig.stripocdn.email/content/guids/CABINET_5127014f192531500fc499f30efa171c/images/34311588845663554.png);background-repeat:repeat;background-position:center top;">
            <tr style="border-collapse:collapse;">
                <td valign="top" style="padding:0;Margin:0;">
                    <table class="es-header" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:#FFA73B;background-repeat:repeat;background-position:center top;">
                        <tr style="border-collapse:collapse;">
                            <td align="center" bgcolor="#453163" style="padding:0;Margin:0;background-color:#453163;">
                                <table class="es-header-body" width="600" cellspacing="0" cellpadding="0" align="center"
                                       bgcolor="transparent"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;">
                                    <tr style="border-collapse:collapse;">
                                        <td align="left"
                                            style="Margin:0;padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:20px;">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="580" valign="top" align="center" style="padding:0;Margin:0;">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                               role="presentation"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="Margin:0;padding-left:10px;padding-right:10px;padding-top:25px;padding-bottom:25px;font-size:0px;">
                                                                    <a href="https://127.0.0.1:5000" target="_blank"
                                                                       style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-size:14px;text-decoration:underline;color:#111111;"><img
                                                                            src="https://ifbvig.stripocdn.email/content/guids/CABINET_5127014f192531500fc499f30efa171c/images/11791588844619730.png"
                                                                            alt
                                                                            style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;"
                                                                            width="261"></a></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;">
                        <tr style="border-collapse:collapse;">
                            <td style="padding:0;Margin:0;background-color:#453163;" bgcolor="#453163" align="center">
                                <table class="es-content-body"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;"
                                       width="600" cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse;">
                                        <td align="left" style="padding:0;Margin:0;">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="600" valign="top" align="center" style="padding:0;Margin:0;">
                                                        <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;background-color:#FFFFFF;border-radius:4px;"
                                                               width="100%" cellspacing="0" cellpadding="0"
                                                               bgcolor="#ffffff" role="presentation">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="Margin:0;padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:35px;">
                                                                    <h1 style="Margin:0;line-height:58px;mso-line-height-rule:exactly;font-family:lato, 'helvetica neue', helvetica, arial, sans-serif;font-size:48px;font-style:normal;font-weight:normal;color:#111111;">
                                                                        Привет!</h1></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td bgcolor="#ffffff" align="center"
                                                                    style="Margin:0;padding-top:5px;padding-bottom:5px;padding-left:20px;padding-right:20px;font-size:0;">
                                                                    <table width="100%" height="100%" cellspacing="0"
                                                                           cellpadding="0" border="0" role="presentation"
                                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                                        <tr style="border-collapse:collapse;">
                                                                            <td style="padding:0;Margin:0px;border-bottom:1px solid #FFFFFF;height:1px;width:100%;margin:0px;"></td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;">
                        <tr style="border-collapse:collapse;">
                            <td align="center" style="padding:0;Margin:0;">
                                <table class="es-content-body"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;"
                                       width="600" cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse;">
                                        <td align="left" style="padding:0;Margin:0;">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="600" valign="top" align="center" style="padding:0;Margin:0;">
                                                        <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-radius:4px;background-color:#FFFFFF;"
                                                               width="100%" cellspacing="0" cellpadding="0"
                                                               bgcolor="#ffffff" role="presentation">
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" bgcolor="#ffffff" align="center"
                                                                    style="Margin:0;padding-top:20px;padding-bottom:20px;padding-left:30px;padding-right:30px;">
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#666666;">
                                                                        Мы рады, что ты теперь с нами!<br>Для начала
                                                                        использования нашего сервиса необходимо подтвердить
                                                                        свой аккаунт. Введи код: </p>
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#453163;">''' + kod + '''</p>
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#666666;">
                                                                        на нашем сайте или просто нажми&nbsp;кнопку
                                                                        ниже.</p></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="Margin:0;padding-left:10px;padding-right:10px;padding-top:35px;padding-bottom:35px;">
                                                                    <span class="es-button-border"
                                                                          style="border-style:solid;border-color:#453163;background:#453163;border-width:1px;display:inline-block;border-radius:2px;width:auto;"><a
                                                                            href="http://127.0.0.1:5000/checkemail/key=''' + kod + '''"
                                                                            class="es-button" target="_blank"
                                                                            style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:helvetica, 'helvetica neue', arial, verdana, sans-serif;font-size:20px;color:#FFFFFF;border-style:solid;border-color:#453163;border-width:15px 25px;display:inline-block;background:#453163;border-radius:2px;font-weight:normal;font-style:normal;line-height:24px;width:auto;text-align:center;">Подтвердить учётную запись</a></span>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-top:20px;padding-left:30px;padding-right:30px;">
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#666666;">
                                                                        Если это не сработало, скопируй&nbsp;и вставь&nbsp;в
                                                                        браузер следующую ссылку:</p></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-top:20px;padding-left:30px;padding-right:30px;">
                                                                    <a target="_blank"
                                                                       href="http://127.0.0.1:5000/checkemail/key=''' + kod + '''"
                                                                       style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-size:18px;text-decoration:underline;color:#453163;">http://127.0.0.1:5000/checkemail/key=''' + kod + '''</a>
                                                                </td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-top:20px;padding-left:30px;padding-right:30px;">
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#666666;">
                                                                        Если у тебя есть какие-либо вопросы, просто ответь&nbsp;на
                                                                        это письмо - мы всегда рады помочь.</p></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="Margin:0;padding-top:20px;padding-left:30px;padding-right:30px;padding-bottom:40px;">
                                                                    <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:18px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;line-height:27px;color:#666666;">
                                                                        С уважением,<br>Команда GAMEPYED</p></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr style="border-collapse:collapse;">
                                        <td align="left"
                                            style="padding:0;Margin:0;padding-left:30px;padding-right:30px;padding-top:40px;">
                                            <table cellpadding="0" cellspacing="0" width="100%"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="540" align="center" valign="top" style="padding:0;Margin:0;">
                                                        <table cellpadding="0" cellspacing="0" width="100%"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;display:none;"></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr style="border-collapse:collapse;">
                                        <td align="left"
                                            style="padding:0;Margin:0;padding-left:30px;padding-right:30px;padding-top:40px;">
                                            <table cellpadding="0" cellspacing="0" width="100%"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="540" align="center" valign="top" style="padding:0;Margin:0;">
                                                        <table cellpadding="0" cellspacing="0" width="100%"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;display:none;"></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;">
                        <tr style="border-collapse:collapse;">
                            <td align="center" style="padding:0;Margin:0;">
                                <table class="es-content-body"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;"
                                       width="600" cellspacing="0" cellpadding="0" align="center">
                                    <tr class="es-mobile-hidden" style="border-collapse:collapse;">
                                        <td style="Margin:0;padding-top:15px;padding-bottom:15px;padding-left:20px;padding-right:20px;background-color:#EFEFEF;"
                                            bgcolor="#efefef" align="left">
                                            <!--[if mso]>
                                            <table width="560" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="178" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left;">
                                                <tr style="border-collapse:collapse;">
                                                    <td class="es-m-p0r" width="178" valign="top" align="center"
                                                        style="padding:0;Margin:0;">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;display:none;"></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td>
                                        <td width="20"></td>
                                        <td width="362" valign="top"><![endif]-->
                                            <table cellspacing="0" cellpadding="0" align="right"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="362" align="left" style="padding:0;Margin:0;">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="padding:0;Margin:0;display:none;"></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td></tr></table><![endif]--></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;">
                        <tr style="border-collapse:collapse;">
                            <td align="center" bgcolor="#453163" style="padding:0;Margin:0;background-color:#453163;">
                                <table class="es-content-body"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;"
                                       width="600" cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse;">
                                        <td style="Margin:0;padding-top:15px;padding-bottom:15px;padding-left:20px;padding-right:20px;background-color:#EFEFEF;"
                                            bgcolor="#efefef" align="left">
                                            <!--[if mso]>
                                            <table width="560" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <td width="180" valign="top"><![endif]-->
                                            <table class="es-left" cellspacing="0" cellpadding="0" align="left"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left;">
                                                <tr style="border-collapse:collapse;">
                                                    <td class="es-m-p0r es-m-p20b" width="180" valign="top" align="center"
                                                        style="padding:0;Margin:0;">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                               role="presentation"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;font-size:0px;"><a
                                                                        target="_blank" href="https://127.0.0.1:5000/"
                                                                        style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-size:18px;text-decoration:underline;color:#FFA73B;"><img
                                                                        src="https://ifbvig.stripocdn.email/content/guids/CABINET_5127014f192531500fc499f30efa171c/images/72111588843576311.png"
                                                                        alt
                                                                        style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;"
                                                                        width="80"></a></td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td>
                                        <td width="20"></td>
                                        <td width="360" valign="top"><![endif]-->
                                            <table cellspacing="0" cellpadding="0" align="right"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="360" align="left" style="padding:0;Margin:0;">
                                                        <table width="100%" cellspacing="0" cellpadding="0"
                                                               role="presentation"
                                                               style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                            <tr style="border-collapse:collapse;">
                                                                <td class="es-m-txt-c" align="center"
                                                                    style="padding:0;Margin:0;padding-top:10px;font-size:0px;background-color:transparent;"
                                                                    bgcolor="transparent">
                                                                    <table class="es-table-not-adapt es-social"
                                                                           cellspacing="0" cellpadding="0"
                                                                           role="presentation"
                                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                                        <tr style="border-collapse:collapse;">
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0;padding-right:30px;">
                                                                                <a target="_blank"
                                                                                   href="mailto:info.gamepyed@gmail.com?subject=%D0%9F%D0%BE%D0%BC%D0%BE%D0%B3%D0%B8%D1%82%D0%B5!%20%D0%9C%D0%B5%D0%BD%D1%8F%20%D0%B4%D0%B5%D1%80%D0%B6%D0%B0%D1%82%20%D0%B2%20%D0%B7%D0%B0%D0%BB%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D1%85%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BC%D0%B0%D1%84%D0%B8%D1%8F%20%D0%B8%20%D0%B7%D0%B0%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D1%8F%D0%B5%D1%82%20%D0%B4%D0%B5%D0%BB%D0%B0%D1%82%D1%8C%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%20%D0%B4%D0%BB%D1%8F%20%D0%B8%D1%85%20%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2!%20%D0%9F%D0%BE%D0%B7%D0%B2%D0%BE%D0%BD%D0%B8%D1%82%D0%B5%20%D0%B2%20911!"
                                                                                   style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-size:18px;text-decoration:underline;color:#FFA73B;"><img
                                                                                        title="Написать info.gamepyed@gmail.com"
                                                                                        src="https://ifbvig.stripocdn.email/content/assets/img/other-icons/circle-black/mail-circle-black.png"
                                                                                        alt="Написать info.gamepyed@gmail.com"
                                                                                        width="64" height="64"
                                                                                        style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;"></a>
                                                                            </td>
                                                                            <td valign="top" align="center"
                                                                                style="padding:0;Margin:0;"><a
                                                                                    target="_blank"
                                                                                    href="https://vk.com/greensmod"
                                                                                    style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-size:18px;text-decoration:underline;color:#FFA73B;"><img
                                                                                    title="ВКонтакте"
                                                                                    src="https://ifbvig.stripocdn.email/content/assets/img/social-icons/circle-black/vk-circle-black.png"
                                                                                    alt="VK" width="64" height="64"
                                                                                    style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;"></a>
                                                                            </td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <!--[if mso]></td></tr></table><![endif]--></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table class="es-content" cellspacing="0" cellpadding="0" align="center"
                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;">
                        <tr style="border-collapse:collapse;">
                            <td style="padding:0;Margin:0;background-color:#453163;" bgcolor="#453163" align="center">
                                <table class="es-content-body"
                                       style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;background:transparent;"
                                       width="600" cellspacing="0" cellpadding="0" align="center">
                                    <tr style="border-collapse:collapse;">
                                        <td align="left" style="padding:0;Margin:0;">
                                            <table width="100%" cellspacing="0" cellpadding="0"
                                                   style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                <tr style="border-collapse:collapse;">
                                                    <td width="600" valign="top" align="center" style="padding:0;Margin:0;">
                                                        <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;background-color:#FFFFFF00;border-radius:4px;"
                                                               width="100%" cellspacing="0" cellpadding="0"
                                                               bgcolor="#ffffff00" role="presentation">
                                                            <tr style="border-collapse:collapse;">
                                                                <td align="center"
                                                                    style="background:transparent;Margin:0;padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:35px;">
                                                                    <h1 style="Margin:0;line-height:58px;mso-line-height-rule:exactly;font-family:lato, 'helvetica neue', helvetica, arial, sans-serif;font-size:48px;font-style:normal;font-weight:normal;color:transparent;background:transparent;"></h1></td>
                                                            </tr>
                                                            <tr style="border-collapse:collapse;">
                                                                <td bgcolor="transparent" align="center"
                                                                    style="Margin:0;padding-top:5px;padding-bottom:5px;padding-left:1000px;padding-right:20px;font-size:0;">
                                                                    <table width="100%" height="100%" cellspacing="0"
                                                                           cellpadding="0" border="0" role="presentation"
                                                                           style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;">
                                                                        <tr style="border-collapse:collapse;">
                                                                            <td style="padding:0;Margin:0px;border-bottom:1px solid #FFFFFF;height:1px;width:100%;margin:0px;"></td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>
    </body>
    </html>'''

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception:
        return False
    else:
        return True


def generator():
    password = ''
    for i in range(12):
        password += choice(chars)
    return password


@app.errorhandler(400)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=400), 400


@app.errorhandler(401)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=401), 401


@app.errorhandler(402)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=402), 402


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=403), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=404), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=406), 405


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=500), 500


@app.errorhandler(502)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=502), 502


@app.errorhandler(503)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=503), 503


@app.errorhandler(504)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=504), 504


@app.errorhandler(505)
def page_not_found(e):
    return render_template('error.html', title="GAMEPYED - OOPS", err=505), 505


@app.route("/")
def main_page():
    return render_template('main_page.html', title="GAMEPYED")


@app.route("/goods")
def goods():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    if current_user.is_authenticated:
        news = session.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", title="GAMEPYED - ОБЪЯВЛЕНИЯ", news=news)


@app.route("/premium")
def premium():
    return render_template('premium.html', title="GAMEPYED - PREMIUM")


@app.route("/about")
def about():
    return render_template('about.html', title="GAMEPYED - О ПРОЕКТЕ")


@app.route("/faq")
def faq():
    return render_template('faq.html', title="GAMEPYED - FAQ")


@app.route('/post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.cost = form.cost.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/goods')
    return render_template('new_post.html', title='GAMEPYED - НОВОЕ ОБЪЯВЛЕНИЕ',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():

        # filename = secure_filename(f.filename)
        # f.save(path.join(
        #     app.instance_path, 'photos', filename
        # ))

        passw = form.password.data
        usname = form.name.data
        List_Psw_Lvl = [sum([len_passw(passw), bad_symvols(passw)]),
                        sum([digit(passw), registr(passw), must_symvols(passw)])]
        for i in usname:
            if i not in name_symvols or len(usname) > 44:
                return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ',
                                       form=form,
                                       message="Имя не соответствует требованиям")
        if List_Psw_Lvl[0] != 2:
            return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ',
                                   form=form,
                                   message="Пароль не соответствует требованиям",
                                   lvl=-1)
        # else:
        #     return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ',
        #                            form=form,
        #                            message="",
        #                            lvl=List_Psw_Lvl[1])
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ',
                                   form=form,
                                   message="Адрес электронной почты уже зарегистрирован")

        while True:
            some = generator()
            if not session.query(User).filter(User.uuid == some).first():
                true_uuid = some
                break
        # print('l')
        user = User(
            name=form.name.data,
            email=form.email.data,
            uuid=true_uuid,
            created_date=date(),
            img=None)

        user.set_password(form.password.data)
        if not mailing(user.email, user.uuid):
            return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ', form=form,
                                   message="Ошибка при отправке письма на электронную почту")
        # print('a')
        session.add(user)
        session.commit()
        # print('la')
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user.id).first()
        # print('la1')
        f = form.img.data
        if f and f.filename.split('.')[-1] in ["png", "jpg", "jpeg"]:
            # print('la2')
            try:
                # print(f.filename)
                with open(f'static/img/users/avatar/{user.id}.jpg', 'wb') as file:
                    file.write(f.read())
            except Exception as e:
                # print(e)
                return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ', form=form,
                                       message="Ошибка при загрузке аватарки")
            else:
                user.img = True
        session.commit()

        return redirect('/accept/{}'.format(user.id))

    return render_template('register.html', title='GAMEPYED - РЕГИСТРАЦИЯ', form=form)


@app.route('/accept/<int:id>', methods=['GET', 'POST'])
def accept(id):
    if current_user.is_authenticated:
        return redirect('/')
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user.is_activate:
        if user.img:
            return render_template('accepted.html', title='GAMEPYED - ВАШ ПОЧТОВЫЙ ЯЩИК ПОДТВЕРЖДЁН', userimg=user.id)
        else:
            return render_template('accepted.html', title='GAMEPYED - ВАШ ПОЧТОВЫЙ ЯЩИК ПОДТВЕРЖДЁН', userimg=False)
    form = AcceptForm()
    if form.validate_on_submit():
        if user and user.uuid == form.check.data:
            user.is_activate = True
            session.commit()
            return redirect(f'/accept/{id}')
        else:
            if user.img:
                return render_template('accept.html', form=form,
                                       title="GAMEPYED - ПОДТВЕРДИТЕ ВАШ ПОЧТОВЫЙ ЯЩИК",
                                       message="Неверный код. Попробуйте ещё раз.", userimg=user.id)
            else:
                return render_template('accept.html', form=form,
                                       title="GAMEPYED - ПОДТВЕРДИТЕ ВАШ ПОЧТОВЫЙ ЯЩИК",
                                       message="Неверный код. Попробуйте ещё раз.", userimg=False)
    if user.img:
        return render_template('accepted.html', title='GAMEPYED - ВАШ ПОЧТОВЫЙ ЯЩИК ПОДТВЕРЖДЁН', userimg=user.id)
    else:
        return render_template('accepted.html', title='GAMEPYED - ВАШ ПОЧТОВЫЙ ЯЩИК ПОДТВЕРЖДЁН', userimg=False)


@app.route('/checkemail/key=<string:code>')
def checkemail(code):
    if current_user.is_authenticated:
        return redirect('/')
    try:
        session = db_session.create_session()
        user = session.query(User).filter(User.uuid == code).first()
        user.is_activate = True
        session.commit()
    except Exception:
        abort(500)
    else:
        return redirect(f'/accept/{user.id}')


@app.route('/user')
@login_required
def user():
    # session = db_session.create_session()
    # user = session.query(User).filter(User.id == id).first()
    return render_template('user.html', title='GAMEPYED - МОЙ ПРОФИЛЬ')
    # Если произведён вход, если id входившего равняется id ссылки и акк, на который заходится по ссылке
    # подтверждён, то можно редактировать информацию. В противном случае можно только увидеть информацию.


@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.id == id:
        form = RedacuserForm()
        if form.validate_on_submit() and form.submit:
            session = db_session.create_session()
            # else:
            #     return render_template('edit_user.html', title='Регистрация',
            #                            form=form,
            #                            message="",
            #                            lvl=List_Psw_Lvl[1])

            if session.query(User).filter(User.email == form.email.data, User.id != id).first():
                return render_template('edit_user.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ПРОФИЛЯ',
                                       form=form,
                                       message="Адрес электронной почты уже зарегистрирован")
            user = session.query(User).filter(User.id == id).first()
            if user:
                user.name = form.name.data
                user.contacts = form.contacts.data
                user.email = form.email.data
                print(form.password.data)
                if len(form.password.data) != 0:
                    if not user.check_password(form.old_password.data):
                        return render_template('edit_user.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ПРОФИЛЯ',
                                               form=form,
                                               message="Введён неверный текущий пароль")
                    if form.old_password.data == form.password.data:
                        return render_template('edit_user.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ПРОФИЛЯ',
                                               form=form,
                                               message="Пароли совпадают")
                    passw = form.password.data
                    List_Psw_Lvl = [sum([len_passw(passw), bad_symvols(passw)]),
                                    sum([digit(passw), registr(passw), must_symvols(passw)])]
                    if List_Psw_Lvl[0] != 2:
                        return render_template('edit_user.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ПРОФИЛЯ',
                                               form=form,
                                               message="Новый пароль не соответствует требованиям")
                    # user.password = form.password.data
                    user.set_password(form.password.data)
                session.commit()
                return redirect('/user')
            else:
                abort(404)
        return render_template('edit_user.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ПРОФИЛЯ', form=form)
    else:
        abort(404)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.status == "A":
        form = AdminForm()
        session = db_session.create_session()
        users = session.query(User)
        if form.validate_on_submit() and form.id.data != "None":
            print(12)
            try:
                user = session.query(User).filter(User.id == int(form.id.data),
                                                  User.status != "A" and User.status != "B").first()
                user.status = "B"
                session.commit()
                return render_template('admin.html', title='личная страница', users=users, form=form)
            except Exception as error:
                print(error)
        return render_template('admin.html', title='личная страница', users=users, form=form)
    else:
        abort(404)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.cost.data = news.cost
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.cost = form.cost.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/goods')
        else:
            abort(404)
    return render_template('new_post.html', title='GAMEPYED - РЕДАКТИРОВАНИЕ ОБЪЯВЛЕНИЯ', form=form)


@app.route('/post_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def post_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/goods')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.is_activate:
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            return redirect('/accept/{}'.format(user.id))
        return render_template('login.html',
                               message="Неверный логин или пароль",
                               title="GAMEPYED - АВТОРИЗАЦИЯ",
                               form=form)
    return render_template('login.html', title='GAMEPYED - АВТОРИЗАЦИЯ', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def main():
    db_session.global_init("db/barahol.sqlite")
    app.run()


if __name__ == '__main__':
    main()
