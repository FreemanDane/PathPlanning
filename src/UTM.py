import math


def utm_conversion(lat, lon):
    """
    ** Input：(a, f, lat, lon, lonOrigin, FN)
    ** a 椭球体长半轴
    ** f 椭球体扁率 f=(a-b)/a 其中b代表椭球体的短半轴
    ** lat 经过Utm投影之前的纬度
    ** lon 经过Utm投影之前的经度
    ** lonOrigin 中央经度线
    ** FN 纬度起始点，北半球为0，南半球为10000000.0m
    ---------------------------------------------
    ** Output:(utm_morthing, UtmEasting)
    ** utm_morthing 经过Utm投影后的纬度方向的坐标
    ** UtmEasting 经过Utm投影后的经度方向的坐标
    ---------------------------------------------
    ** 功能描述：Utm投影
    ** 作者： ace Strong
    ** 单位： cca NUaa
    ** 创建日期：2008年7月19日
    ** 版本：1.0
    ** 本程序实现的公式请参考
    ** "coordinate conversions and transformations including Formulas" p35.
    ** & http://www.uwgb.edu/dutchs/UsefulData/UtmFormulas.htm
    """
    # e表示WGS84第一偏心率,e_square表示e的平方f
    f = 0.003352309884
    lon_origin = 0
    FN = 0
    e_square = 2 * f - f * f
    a = 6378136.49
    k0 = 0.9996
    # 确保longtitude位于-180.00----179.9之间
    lon_temp = (lon + 180) - int((lon + 180) / 360) * 360 - 180
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon_temp)
    lon_origin_rad = math.radians(lon_origin)
    e2_square = e_square / (1 - e_square)
    v = a / math.sqrt(1 - e_square * math.sin(lat_rad) ** 2)
    t = math.tan(lat_rad) ** 2
    c = e2_square * math.cos(lat_rad) ** 2
    a = math.cos(lat_rad) * (lon_rad - lon_origin_rad)
    m = a * ((1 - e_square / 4 - 3 * e_square ** 2 / 64 - 5 * e_square ** 3 / 256) * lat_rad
             - (3 * e_square / 8 + 3 * e_square ** 2 / 32 + 45 * e_square ** 3 / 1024) * math.sin(2 * lat_rad)
             + (15 * e_square ** 2 / 256 + 45 * e_square ** 3 / 1024) * math.sin(4 * lat_rad)
             - (35 * e_square ** 3 / 3072) * math.sin(6 * lat_rad))
    # x
    utm_x = k0 * v * (a + (1 - t + c) * a ** 3 / 6 + (5 - 18 * t + t ** 2 + 72 * c
                                                      - 58 * e2_square) * a ** 5 / 120) + 500000.0
    # y
    utm_y = k0 * (m + v * math.tan(lat_rad) * (a ** 2 / 2 + (5 - t + 9 * c + 4 * c ** 2) *
                                               a ** 4 / 24 + (61 - 58 * t + t ** 2
                                                              + 600 * c - 330 * e2_square) * a ** 6 / 720))
    utm_y += FN
    print(utm_x, utm_y)
    return utm_x, utm_y


utm_conversion(140, 130)



