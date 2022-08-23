# 상승장 형태에서 변화가 비교적 심한 종목일 경우 적용
class 변화심한그래프():
    # 초기 값 지정
    def __init__(self):
        self.int_보유주식수 = 0
        self.int_전일가 = 0
        self.dou_누적률 = 0.0
        self.dou_전일기준등락률 = 0
        self.dou_고정비율 = 20.0 # 주식 종목별 변경 필요

    # set
    def set_int_보유수량(self, int_보유주식수):
        self.int_보유주식수 = int_보유주식수
    def set_dou_누적률(self, dou_누적률):
        self.dou_누적률 = dou_누적률
    def set_int_보유수량(self, int_보유주식수):
        self.int_보유주식수 = int_보유주식수
    def set_int_전일가(self, int_전일가):
        self.int_전일가 = int_전일가
    
    def 내부변수_보여주기(self):
        print("현재 보유수량 : ", self.int_보유주식수, ", 누적률 : ", self.dou_누적률,
                        ", 전일가 : ", self.int_전일가)

    # 현재 시세를 입력받아 매수, 매도, 대기 를 판단해서 알려주는 함수
    def 거래행동판단(self, int_주가):
        # ex) 현재 주가가 8000원, 전일 가격이 10000원이면 전일기준 등락률은 -20% (-2000 / 10000 * 100)가 됨
        self.dou_전일기준등락률 = ((int_주가-self.int_전일가)/self.int_전일가) * 100

        # 전일 등략률을 누적함
        self.dou_누적률 = self.dou_누적률 + self.dou_전일기준등락률

        # 내부 변수 현황 출력
        #print("현재가 : "+ str(int_주가) +", 전일가 대비 등락률 :" + str(dou_전일기준등락률))
        #self.내부변수_보여주기()
        
        # 누적률이 고정비율 이상인 경우 전량 매도 후 공통 변수 초기화
        if self.dou_누적률 >= self.dou_고정비율:
            int_행동 = -1 * self.int_보유주식수
            self.dou_누적률 = 0.0 
            self.int_보유주식수 = self.int_보유주식수 + int_행동

        # 누적률이 -20%(-고정비율) 이하인 경우, 현재 누적률을 보유 주식수에 곱한 수 만큼 추가 매수
        elif self.dou_누적률 <= -1 * self.dou_고정비율:
            int_행동 = int(self.int_보유주식수 * ((self.dou_누적률/100) * -1))
            self.set_int_보유수량(self.int_보유주식수+int_행동) 

        # 누적률이 +고정비율과 -고정비율 사이일 경우(20% ~ -20%) 행동은 없음
        else:
            int_행동 = 0

        # 결정된 행동을 반환
        return int_행동

    def 현재가치판단(self, Ticker):
        print("미구현 동작입니다.")

def Simulate_변화심한그래프(str_ticker, str_startdate):
    #str_ticker = "GOOGL"
    #str_startdate = "2021-03-01"
    str_enddate = datetime.now()

    yf_Ticker = yf.Ticker(str_ticker) #AAPL, TSLA, GOOGL
    close_TickerData = yf_Ticker.history(start=str_startdate, end=str_enddate, interval="1d")['Close']

    int_최초구매수량 = 10 # 주식 종목별 최적화 필요 변수
    dou_시작주가 = close_TickerData[0]
    dou_최초투자금 = int_최초구매수량 * dou_시작주가

    # class set
    f = 변화심한그래프()
    f.set_int_보유수량(int_최초구매수량)
    f.set_int_전일가(dou_시작주가)

    print("\n초기값")
    print("Tiker :" + str_ticker + ", Start : " + str_startdate + ", Now : " + str_enddate.strftime('%Y-%m-%d') )
    f.내부변수_보여주기()
    print("")

    # 입력 기준 7일 단위로 값 가져오기 
    list_7일단위값 = []
    for i in range(1, len(close_TickerData)):    
        if i%7 == 0:
            list_7일단위값.append(close_TickerData[i])

    # 시작
    cnt = 1 
    int_전체추가투자금액 = 0

    # 시뮬레이션 Start
    for int_현재주가 in list_7일단위값:
        int_행동 = f.거래행동판단(int_현재주가)
    
        if int_행동 == 0:
            print(str(cnt) + "회 행동 : 대기")
            print("현재가 : "+ str(int_현재주가) +", 전일가 대비 등락률 :" + str(f.dou_전일기준등락률))
            print("현재 보유수량 : ", f.int_보유주식수, ", 누적률 : ", f.dou_누적률, ", 전일가 : ", f.int_전일가)
        
        elif int_행동 > 0:
            print(str(cnt) + "회 행동 : ", int_행동, "주 매수 -> 현재보유 주식 수(주) : " + str(f.int_보유주식수) + ", 추가 투자금($) : " + str(int_행동 * int_현재주가))
            int_전체추가투자금액 += (int_행동 * int_현재주가)
   
        else:
            print(str(cnt) + "회 행동 : 전량매도(", int_행동, "주), 매도 금액($) : " + str(int_행동*int_현재주가*-1))
            print("  투자 기간 : " + str_startdate + " ~ " + (datetime.strptime(str_startdate,"%Y-%m-%d") + timedelta(days=(cnt*7))).strftime('%Y-%m-%d') )
            print("  최초 투자금액 : " + str(dou_최초투자금))
            print("  추가 투자금액 : " + str(int_전체추가투자금액))
            print("  전체 투자금액 : " + str(dou_최초투자금+int_전체추가투자금액))
            print("  손익 : " + str((int_행동*int_현재주가*-1) - (dou_최초투자금 + int_전체추가투자금액)))
            break
    
        f.set_int_전일가(int_현재주가)
        print("")
        cnt += 1
