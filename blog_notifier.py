"""
はてなブログの執筆済み記事件数取得機能を担当するクラス
"""
import requests
from xml.etree import ElementTree as ET


class BlogNotifier:
    """はてなブログの執筆済み記事件数を取得するクラス"""
    
    def __init__(self, blog_domain, username, api_key):
        """
        BlogNotifierを初期化する
        
        Args:
            blog_domain (str): はてなブログのドメイン (例: "username.hatenablog.com")
            username (str): はてなブログのユーザー名
            api_key (str): はてなブログのAPIキー
        """
        self.blog_domain = blog_domain
        self.username = username
        self.api_key = api_key
        self.base_url = f"https://blog.hatena.ne.jp/{username}/{blog_domain}/atom"
    
    def get_published_posts_count(self):
        """
        執筆済み記事の件数を取得する
        
        Returns:
            int: 執筆済み記事の件数
        """
        try:
            # はてなブログのAtomPub APIから記事一覧を取得
            response = requests.get(
                f"{self.base_url}/entry",
                auth=(self.username, self.api_key),
                timeout=30
            )
            response.raise_for_status()
            
            # XMLをパースして記事数をカウント
            root = ET.fromstring(response.content)
            
            # 名前空間の定義
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'app': 'http://www.w3.org/2007/app'
            }
            
            # entryタグの数をカウント
            entries = root.findall('.//atom:entry', namespaces)
            return len(entries)
            
        except requests.RequestException as e:
            print(f"API呼び出しエラー: {e}")
            return 0
        except ET.ParseError as e:
            print(f"XMLパースエラー: {e}")
            return 0
        except Exception as e:
            print(f"予期しないエラー: {e}")
            return 0
    
    def get_posts_summary_message(self):
        """
        執筆済み記事の件数サマリーメッセージを生成する
        
        Returns:
            str: サマリーメッセージ
        """
        count = self.get_published_posts_count()
        if count > 0:
            return f"📝 *現在の執筆済み記事数*: {count}件"
        else:
            return "📝 *執筆済み記事の取得に失敗しました*"
