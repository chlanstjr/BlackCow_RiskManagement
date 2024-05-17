import schedule
import time
import datetime
import yfinance as yf
import asyncio
import telegram
import datetime
import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

korea_timezone = pytz.timezone('Asia/Seoul')

def run():
    x = datetime.datetime.now(korea_timezone)
    start_date = (x - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (x + datetime.timedelta(days=7)).strftime('%Y-%m-%d')

    start_money = 7745106
    # 수수료 및 세금
    charge_fee = 0.00015
    tax_fee = 0.002

    # RP, 현재 RP 가격 불러오도록 바꿔야함. RP는 고정수익률이니 수익률 측정은 의미 없음.
    rp = 0
    # 현금
    cash = 863274
    # 주식
    stock_total = 0
    # sk하이닉스, 한국카본, 유진테크, 팅크웨어, 켐트로닉스, 테스, 서연이화
    stock_ticker = ['000660.KS','218410.KQ','084370.KQ','084730.KQ','089010.KQ','095610.KQ','200880.KS','009150.KS','348340.KQ','042660.KS']
    stock_name = ['sk하이닉스', 'RFHIC', '유진테크', '팅크웨어', '켐트로닉스', '테스', '서연이화', '삼성전기','뉴로메카','한화오션']

    stock_endprice = []
    stock_cnt = [4,39,10,37,49,26,30,7,9,16]
    stock_purchase_price = [131013,16717,42278,15549,23681,20438,16197,149857,39050,30350]
    stock_return = []

    # 포트폴리오 평가금
    evaluation_money = 0
    # 종목별 평가금
    stock_money = []

    # 종목별 종가
    for i in range(len(stock_ticker)):
        stock_endprice.append(yf.download(stock_ticker[i],start=start_date,end=end_date, progress=False)['Close'].values[-1])

    # 각 종목별 종가 * 주식수 -(세금 + 수수료)
    for i in range(len(stock_ticker)):
        stock_money.append(stock_endprice[i]*stock_cnt[i]*(1-charge_fee-tax_fee))

    # 수익률
    for i in range(len(stock_ticker)):
        stock_return.append((stock_money[i]-stock_purchase_price[i]*stock_cnt[i])/stock_purchase_price[i]/stock_cnt[i])

    # 총 평가금
    for i in range(len(stock_ticker)):
        stock_total += stock_money[i]
    evaluation_money = stock_total + rp + cash

    msg_result = ''

    # 날짜
    msg_result += str(x.year)+'년'+str(x.month)+'월'+str(x.day)+'일'+'\n\n'

    # 평가금 기준
    msg_result += '포트폴리오 수익률 : ' + str(round((evaluation_money/start_money-1)*100, 2)) + '%' +'\n\n'

    msg_result += '<종목별비중>'+'\n'
    msg_result += 'RP : ' + str(round(rp/evaluation_money*100, 2)) + '%' +'\n'
    msg_result += '현금 : '+str(round(cash/evaluation_money*100, 2))+'%'+'\n'
    for i in range(len(stock_ticker)):
        msg_result += stock_name[i]+' : '+str(round(stock_money[i]/evaluation_money*100, 2))+'%'+'\n'
    # 종목별 수익률
    msg_result +='\n'+'<종목별 수익률>'+'\n'
    for i in range(len(stock_ticker)):
        msg_result += stock_name[i]+' : '+str(round(stock_return[i]*100,2))+'%'+'\n\n'

    msg_result += 'RP : ' + str(round(rp)) + '원(RP 매수 금액)' +'\n'
    msg_result += '현금 : '+str(round(cash))+'원'+'\n'

    return msg_result

async def main():
    token = '6819434018:AAFkT0OG-Xsht6wZc4Hxqr8Xy-iXTpDcxP0'
    bot = telegram.Bot(token)
    await bot.send_message(chat_id="-4026107937", text=run())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'cron', hour=17, timezone = korea_timezone)
    scheduler.start()
    while True:
        await asyncio.sleep(1000)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

print(run())