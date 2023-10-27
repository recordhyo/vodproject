import requests, json, csv, re
csv_file_path = './../test.csv'


global Details
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4ZmU3Zjc0NDkzOWViOGYwZmY4ZGNlMGY2OTIzN2Y3ZiIsInN1YiI6IjY1Mzc4MDM3NDFhYWM0MDBhYTA3ZTBlNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RfZj_QvZtiLrqhs7crrHBukRA0elNetuc9yWYdos5sg"
}
def SearchVODInfo(name) :
    VOD = []

    #프로그램 제목으로 1차 검색 - apiid, 제목, 줄거리, imgpath, category(영화/tv)
    url1 = "https://api.themoviedb.org/3/search/multi"
    params1 = {
        "api_key": "8fe7f744939eb8f0ff8dce0f69237f7f",
        "language": "ko",
        "query": name,
        "include_adult": True
    }
    response1 = requests.get(url1, headers=headers, params=params1)

    if 'name' in response1.json()['results'][0]:
        Details = {
        'apiid': int(response1.json()['results'][0]['id']),
        'name' : response1.json()['results'][0]['name'],
        'description' : response1.json()['results'][0]['overview'],
        'imgpath': response1.json()['results'][0]['poster_path'],
        'category': response1.json()['results'][0]['media_type']
        }
    else:
        Details = {
        'apiid': int(response1.json()['results'][0]['id']),
        'name' : response1.json()['results'][0]['title'],
        'description' : response1.json()['results'][0]['overview'],
        'imgpath': response1.json()['results'][0]['poster_path'],
        'category': response1.json()['results'][0]['media_type']
        }
    #VOD.append(Details)
    json_string = json.dumps(Details, ensure_ascii=False, indent=2)
    #print(json_string)
    #print(response.json()['results'][0])


    #apiid 로 credits 검색 - 감독(crew - director), 등장인물(cast)
    #영화 검색
    if Details['category']=='movie' :
        movie_id = Details['apiid']
        urlmovie = (f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko")
        responsem = requests.get(urlmovie, headers=headers)

        #crew가 0이 아닐 경우
        if (len(responsem.json()['crew'])!=0)  :
            for i in range(len(responsem.json()['crew'])) :
                #crew중 job이 Director이고
                if responsem.json()['crew'][i]['job']=="Director" :
                    #이름이 한글이면 바로 Dict에 삽입
                    if re.match('[가-힣]', responsem.json()['crew'][i]['name']) :
                        Details['director'] = responsem.json()['crew'][i]['name']
                    #이름이 한글이 아니면 영to한 변환함수 호출 후 삽입
                    else :
                        person_id = responsem.json()['crew'][i]['id']
                        Details['director'] = PersonEngtoKor(person_id)
                    # 감독이 여러 명일 경우 1명만 찾고 break
                    break
        #cast가 0이 아닐 경우
        if (len(responsem.json()['cast'])!=0) :
            #cast가 1명이면 cast의 사람id로 영to한 변환함수 호출하여 배우에 삽입
            if (len(responsem.json()['cast'])==1) :
                person_id = responsem.json()['cast'][0]['id']
                Details['actor'] = PersonEngtoKor(person_id)
            #cast가 여러명이면 2명까지만 사람id로 영to한 변환함수 호출하여 배우에 삽입
            else:
                person_id = responsem.json()['cast'][0]['id']
                actor1 = PersonEngtoKor(person_id)
                person_id = responsem.json()['cast'][1]['id']
                actor2 = PersonEngtoKor(person_id)
                actorstring = (f"{actor1}, {actor2}")
                Details['actor'] = actorstring
            #print(json_string)

    #TV프로그램 검색
    if Details['category'] == 'tv':
        series_id = Details['apiid']
        urltv = (f"https://api.themoviedb.org/3/tv/{series_id}/credits?language=ko")
        responsetv = requests.get(urltv, headers=headers)

        if (len(responsetv.json()['crew'])!=0) :
            for i in range(len(responsetv.json()['crew'])) :
                if responsetv.json()['crew'][i]['job']=="Director" and re.match('[가-힣]', responsetv.json()['crew'][i]['name']) :
                    Details['director'] = responsetv.json()['crew'][i]['name']
                elif responsetv.json()['crew'][i]['job']=="Director" and re.match('[^가-힣]', responsetv.json()['crew'][i]['name']) :
                    person_id = responsetv.json()['crew'][i]['id']
                    Details['director'] = PersonEngtoKor(person_id)
                break

        if (len(responsetv.json()['cast'])!=0):
            if (len(responsetv.json()['cast'])==1) :
                person_id = responsetv.json()['cast'][0]['id']
                Details['actor'] = PersonEngtoKor(person_id)
            else :
                person_id = responsetv.json()['cast'][0]['id']
                actor1 = PersonEngtoKor(person_id)
                person_id = responsetv.json()['cast'][1]['id']
                actor2 = PersonEngtoKor(person_id)
                actorstring = (f"{actor1}, {actor2}")
                Details['actor'] = actorstring


    json_string = json.dumps(Details, ensure_ascii=False, indent=2)
    print(json_string)


def PersonEngtoKor(person_id) :
    urlperson = (f"https://api.themoviedb.org/3/person/{person_id}?language=ko")
    responsep = requests.get(urlperson, headers=headers)
    if len(responsep.json()['also_known_as'])!=0:
        for j in range(len(responsep.json()['also_known_as'])):
            if re.match('[가-힣]', responsep.json()['also_known_as'][j]):
                return responsep.json()['also_known_as'][j]
    else :
        return responsep.json()['name']



with open(csv_file_path, 'r', encoding='utf8') as f :
    reader = csv.reader(f)

    if __name__ == '__main__':
        for line in reader:
            SearchVODInfo(line[1])