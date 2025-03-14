import app
import cloudinary.uploader
import cloudinary.api
import cloudinary

cloudinary.config(
    cloud_name = 'djskafzqr',
    api_key = '965529918623125',
    api_secret = 'kbAOynBOiewYoLA76pOWQo4ktV0'
)


if __name__ == '__main__':
    img_path = r"C:\Users\MTHANG\Downloads\RR-Standard-2-Queen.jpg"
    res = cloudinary.uploader.upload(img_path)
    print(res['secure_url'])
    #bg https://res.cloudinary.com/djskafzqr/image/upload/v1734439997/wfi0npcwfrhbz2chvmhv.jpg
    #r1 https://res.cloudinary.com/djskafzqr/image/upload/v1734441270/n0klrik4czzoecowdeis.jpg
    #r2 https://res.cloudinary.com/djskafzqr/image/upload/v1734441326/gtzf0lnc00kurtqprm2y.jpg
    #r3 https://res.cloudinary.com/djskafzqr/image/upload/v1734441388/qkrdcagoaiwefnxn4s5f.jpg
    #r4 https://res.cloudinary.com/djskafzqr/image/upload/v1734441475/qallwlk0gwhg4vnn4szb.jpg
    #r5 https://res.cloudinary.com/djskafzqr/image/upload/v1734441517/tf5zfpv0zzjjkrcisynt.jpg
    #r6 https://res.cloudinary.com/djskafzqr/image/upload/v1734441555/ljovwdfzirrnk7c7orns.jpg