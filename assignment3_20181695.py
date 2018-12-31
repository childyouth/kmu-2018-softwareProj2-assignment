import pickle

################-----------------------------------------------------------------------------------------

#교수님의 예제파일의 dat파일은 데이터의 int형 피클링이 안되어 있기 때문에 첫 실행시 dat파일을 지우고 실행

################-----------------------------------------------------------------------------------------


################=========================================================================================

# --- : 수정이 필요한 내용

################=========================================================================================

dbfilename = 'assignment3_20181695.dat'


commands = """? : 명령어 조회
add (name) (age) (score) : 학생의 이름, 나이, 성적 추가
del (names ...) : 이름에 해당하는 학생(들) 삭제
show (option) |option;Name, Age, Score| : 이름/나이/점수를 기준으로 내림차순 전체 조회
find (names ...) : 이름에 해당하는 학생(들) 조회
inc (names ...) (amount) : 이름에 해당하는 학생(들) 의 성적을 숫자만큼 증감
quit : 변경된 데이터들을 파일에 저장함. 강제종료시 저장되지 않음
          
이름을 사용하는 모든 명령은 같은 이름을 가진 사람들에게 영향이 있음."""

def readScoreDB():
    try:
        fH = open(dbfilename, 'rb')
    except FileNotFoundError as e:
        print("New DB: ", dbfilename)                                                               # 데이터 파일이 없더라도 quit으로 종료시 dbfilename변수의 값으로 파일이 생성됨을 알려줌
        return []

    scdb = []
    try:
        scdb =  pickle.load(fH)
    except:
        print("Empty DB: ", dbfilename)
    else:
        print("Open DB: ", dbfilename)
    fH.close()
    return scdb


# write the data into person db
def writeScoreDB(scdb):
    fH = open(dbfilename, 'wb')
    pickle.dump(scdb, fH)                                                                            # scdb의 내용을 파일에 덤핑
    fH.close()


def doScoreDB(scdb):
    while(True):
        inputstr = (input("Score DB > "))
        if inputstr == "": continue
        parse = inputstr.split(" ")                                                                  # 공백으로 인자 구별
                                                                                                     # --- 스페이스바가 붙여져서 여러개 들어갈 경우 의미없는 리스트 아이템이 생성됨
        if parse[0] == 'add':
            try:
                record = {'Name':parse[1], 'Age':int(parse[2]), 'Score':int(parse[3])}
            except IndexError as e:
                print("리스트의 인덱스를 벗어났습니다. (" + e + ")")
            except ValueError as e:
                print("자료형의 처리에 있어 오류가 발생했습니다. (" + e +")")
            except:
                print("\'add\' must be executed in the order of Name, Age, Score. // add (name) (age) (score)")
            else:
                scdb += [record]
        elif parse[0] == 'del':
            nameNotFound = []
            nameTotalDel = []
            for k in parse[1:]:                                                                     # 여러명을 동시에 지우기 위해
                flagOverlap = False
                cnt = 0;
                for p in sorted(scdb, key=lambda person: person['Name']):                          # add 하면서 정렬이 되지 않았으므로 정렬 추가
                    if p['Name'] == k:
                        scdb.remove(p)
                        cnt += 1;
                        flagOverlap = True
                    elif flagOverlap:                                                                # 같은이름이 끝났을 때 루프 종료
                        break
                if not flagOverlap:                                                                  # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
                    nameNotFound += [k]
                nameTotalDel += [{"Name":k,"Cnt":cnt}]
            for t in nameTotalDel:
                print(t["Name"]," 총 ",t["Cnt"],"명 삭제")
            for p in nameNotFound:
                print("Student Name \"" + p + "\" not found")

        elif parse[0] == 'show':
            sortKey ='Name' if len(parse) == 1 else parse[1]                                        # 삼항 연산자/ 입력 길이가 1이면 key로서 Name을, 뒤에 추가 입력이 있으면 그것(Name, Age, Score)을 기준으로
            showScoreDB(scdb, sortKey)
        elif parse[0] == 'find':
            findKey =[] if len(parse) == 1 else parse
            findScoreDB(scdb, findKey)
        elif parse[0] == 'inc':
            names =[] if len(parse) == 1 else parse
            incScoreDB(scdb, names)
        elif parse[0] == '?':
            print(commands)
        elif parse[0] == 'quit':
            break
        else:
            print("Invalid command: " + parse[0])


def showScoreDB(scdb, keyname):
    try:
        for p in sorted(scdb, key=lambda person: person[keyname]):                                 # 람다식/ scdb의 내용을 기준값을 비교해 정렬
            for attr in sorted(p):                                                                  # scdb의 아이템 내부 속성들 정렬(알파벳순 age, name, score
                print(attr + "=" + str(p[attr]), end=' ')
            print()
    except IndexError as e:
        print("리스트의 인덱스를 벗어났습니다. (" + e + ")")
    except ValueError as e:
        print("자료형의 처리에 있어 오류가 발생했습니다. (" + e +")")
    except:
        print("There is 3 options in \'show\' commands. You should use [Name, Age or Score] to the option. // show (option) |option;Name, Age, Score|")

def findScoreDB(scdb, findKey):
    nameNotFound = []
    cnt = 0;
    for k in findKey[1:]:                                                                           # 여러명을 찾기 위해 리스트로 받아옴 (0번째는 명령어)
        flagOverlap = False
        for p in sorted(scdb, key=lambda person: person['Name']):                                  # 람다식/ scdb의 내용을 기준값을 비교해 정렬
            if p['Name'] == k:
                for attr in sorted(p):                                                              # scdb의 아이템 내부 속성들 정렬(알파벳순 age, name, score
                    print(attr + "=" + str(p[attr]), end=' ')
                print()
                cnt += 1;
                flagOverlap = True
            elif flagOverlap:                                                                        # 같은이름이 끝났을 때 루프 종료
                break
        if not flagOverlap:                                                                          # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
            nameNotFound += [k]
    print("총 %d명 발견"%cnt);
    for p in nameNotFound:
        print("Student Name \"" + p + "\" not found")

def incScoreDB(scdb, names):                                                                    # --- 중복된 이름 중 원치않는 인물의 점수가 수정될 수 있기 때문에 매커니즘의 수정 필요 ---
    try:
        amount = int(names.pop())                                                                 # 입력의 마지막에 증감할 수치가 있다 (규칙)
    except IndexError as e:
        print("리스트의 인덱스를 벗어났습니다. (" + e + ")")
    except ValueError as e:
        print("자료형의 처리에 있어 오류가 발생했습니다. (" + e +")")
    except:
        print("\'inc\' must have amount(int) at the end of command. // inc (names ...) (amount)")
    else:
        nameNotFound = []
        for k in names[1:]:
            flagOverlap = False
            for p in sorted(scdb, key=lambda person: person['Name']):                             # 람다식/ scdb의 내용을 기준값을 비교해 정렬
                if p['Name'] == k:
                    p['Score'] += amount
                    flagOverlap = True
                elif flagOverlap:                                                                   # 같은이름이 끝났을 때 루프 종료
                    break
            if not flagOverlap:                                                                         # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
                nameNotFound += [k]
        for p in nameNotFound:
            print("Student Name \"" + p + "\" not found")

print("command \'?\' to look up all command")
scoredb = readScoreDB()
doScoreDB(scoredb)
writeScoreDB(scoredb)