from spider import Music
import getopt,sys,logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

def menu():
    print('-c <--comments> -l <--lyric> -m <--mp3>')
    print('-c <--comments>   爬取评论')
    print('-l <--lyric>      爬取歌词')
    print('-m <--mp3>        爬取歌曲地址')
    print("示例:python main.py -c 歌曲id")
    print("python main.py -c 歌曲id(若id为108390)")

def main(argv):
    if not bool(argv):
        menu()
    try:
        try:
            options, args = getopt.getopt(argv, "hl:m:c:", ["lyric=", "mp3=", "comments="])
        except getopt.GetoptError:
            menu()
            sys.exit(2)
        for option, arg in options:
            if option == '-h':
                menu()
                sys.exit()
            elif option in ('-l', '--lyric'):
                id = arg
                print(id)
                Music().get_song_params(id=id, musicType="lyric")
            elif option in ('-m', '--mp3'):
                id = arg
                Music().get_song_params(id=id, musicType="mp3")
            elif option in ('-c', '--comments'):
                id = arg
                Music().get_song_params(id=id, musicType="comments")
    except:
        logging.info("请安装reids数据库，然后找到本目录proxy_pool下Run目录")

if __name__ == '__main__':
    main(sys.argv[1:])