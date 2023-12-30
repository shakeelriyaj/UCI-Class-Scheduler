#deqh tyjn tmhs jnuy
import smtplib

def emailSender(message):
    host = "smtp.gmail.com"
    port = 587
    from_mail = "shakeelpythontest@gmail.com"
    to_mail = "imran.riyaj@gmail.com"
    password = "deqh tyjn tmhs jnuy"
    
    msg = (f"Subject: {message}\n")

    smtp = smtplib.SMTP(host, port)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")
    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection : {status_code} {response}")
    status_code, response = smtp.login(from_mail, password)
    print(f"[*] Logging in : {status_code} {response}")
    smtp.sendmail(from_mail, to_mail, msg)
    print("Mail Sent Successfully!")
    smtp.quit()