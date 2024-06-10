import requests

# 發送帶有 Authorization 標頭的 GET 請求
def send_request(url, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# 美化並打印輸出
def beautify_currentwar_output(data):
    print("戰爭狀態:", data['state'])
    print("隊伍大小:", data['teamSize'])
    print("每個成員的攻擊次數:", data['attacksPerMember'])
    print("準備開始時間:", data['preparationStartTime'])
    print("戰爭開始時間:", data['startTime'])
    print("戰爭結束時間:", data['endTime'])
    
    print("\n=== 我方部落 ===")
    clan = data['clan']
    print("部落標籤:", clan['tag'])
    print("部落名稱:", clan['name'])
    print("部落等級:", clan['clanLevel'])
    print("攻擊次數:", clan['attacks'])
    print("星星數量:", clan['stars'])
    print("摧毀百分比:", clan['destructionPercentage'])
    print("成員:")
    sorted_members = sorted(clan['members'], key=lambda x: x['mapPosition'])
    for member in sorted_members:
        print(f"  - 名稱: {member['name']}, 標籤: {member['tag']}, 大本營等級: {member['townhallLevel']}, 地圖位置: {member['mapPosition']}, 被攻擊次數: {member['opponentAttacks']}")

    print("\n=== 對方部落 ===")
    opponent = data['opponent']
    print("部落標籤:", opponent['tag'])
    print("部落名稱:", opponent['name'])
    print("部落等級:", opponent['clanLevel'])
    print("攻擊次數:", opponent['attacks'])
    print("星星數量:", opponent['stars'])
    print("摧毀百分比:", opponent['destructionPercentage'])
    print("成員:")
    sorted_members = sorted(opponent['members'], key=lambda x: x['mapPosition'])
    for member in sorted_members:
        print(f"  - 名稱: {member['name']}, 標籤: {member['tag']}, 大本營等級: {member['townhallLevel']}, 地圖位置: {member['mapPosition']}, 被攻擊次數: {member['opponentAttacks']}")

# 主程序
if __name__ == '__main__':
    currentwar_url = 'https://api.clashofclans.com/v1/clans/%23RP0CQLQR/currentwar'
    api_key = 'KEY'
    response = send_request(currentwar_url, api_key)
    # print(response)
    beautify_currentwar_output(response)
