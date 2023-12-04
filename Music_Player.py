import time
import random
import csv

class Song:
    def __init__(self, song_id, song_name, song_length):
        self.song_id = song_id
        self.song_name = song_name
        self.song_length = song_length
        
    def __str__(self):
        return str({'song_id':self.song_id, 
                    'song_name':self.song_name, 
                    'song_length':self.song_length})
        
        
class ListNode:
    def __init__(self, song:Song):
        self.song = song
        self.next = None
        
    def __str__(self):
        return str(self.song)
    
    
class LinkedList:
    def __init__(self):
        self.head_node = None
        self.count = 0
    
    def traversal(self):
        if self.head_node is None:
            return
        
        temp_node = self.head_node
        
        while(temp_node != None):
            print(temp_node.song)
            time.sleep(2)
            temp_node = temp_node.next
        
        time.sleep(2)
        
        return
    
    def insert_at_start(self, node):
        if self.head_node is None:
            self.head_node = node
            self.count = self.count + 1
            return True
        
        node.next = self.head_node
        self.head_node = node
        
        return True
        
    def insert_after(self, song_name, node):
        temp_node = self.head_node
        
        while(temp_node.song.song_name!=song_name):
            temp_node = temp_node.next
            
        if temp_node is None:
            return False
        else:
            if temp_node.next == None:
                temp_node.next = node
            else:
                node.next = temp_node.next
                temp_node.next = node
            
            return True
        
    def insert_before(self, song_name, node):
        temp_node = self.head_node
        prev_node = None
        
        while(temp_node.song.song_name!=song_name):
            prev_node = temp_node
            temp_node = temp_node.next
        
        if temp_node == None:
            return False
        
        if prev_node == None:
            node.next = self.head_node
            self.head_node = node
            return True
        
        prev_node.next = node
        node.next = temp_node
        
        return True
    
    def delete_song(self, song_name):
        if self.head_node is None:
            return True
        
        temp_node = self.head_node
        prev_node = None
        
        while(temp_node.song.song_name!=song_name):
            prev_node = temp_node
            temp_node = temp_node.next
        
        if temp_node is None:
            return False
        
        if prev_node is None:
            self.head_node = None
            return True
        
        prev_node.next = temp_node.next
        
        return True
    
    def sort_list(self):
        if self.head_node is None:
            return
        
        nodes_list = list()
        
        temp_node = self.head_node
        
        while(temp_node is not None):
            nodes_list.append(ListNode(temp_node.song))
            temp_node = temp_node.next
            
        nodes_list = sorted(nodes_list, key = lambda node : node.song.song_name, reverse=True)
        self.head_node = None
        
        for node in nodes_list:
            self.insert_at_start(node)
        
        return
    
    def shuffle_song(self):
        if self.head_node is None:
            return None
        
        nodes_list = list()
        
        temp_node = self.head_node
        
        while(temp_node):
            nodes_list.append(ListNode(temp_node.song))
            temp_node = temp_node.next
            
        return nodes_list[random.randint(0, len(nodes_list)-1)]
    
class PlayList:
    def __init__(self, id, playlist_name, linked_list:LinkedList):
        self.playlist_id = id
        self.playlist_name = playlist_name
        self.playlist_linked_list = linked_list
        
    def get_playlist(self):
        return self.playlist_linked_list
    
    def get_playlist_name(self):
        return self.playlist_name
    
    def get_playlist_id(self):
        return self.playlist_id
        
class MusicPlayer:
    def __init__(self):
        self.playlists = list()
        
    def add_playlist(self, new_playlist:PlayList):
        self.playlists.append(new_playlist)
        
    def play_playlist(self, playlist_name):
        for playlist in self.playlists:
            if playlist.get_playlist_name() == playlist_name:
                playlist.get_playlist().traversal()
            else:
                print('No such playlist exists in the Music Player')
        
    def delete_song_from_playlist(self, playlist_name, song_name):
        playlist = self.search_playlist_by_name(playlist_name)
        if playlist is None:
            print("No such playlist exists in the Music Player.")
            return
        playlist.get_playlist().delete_song(song_name)
        return
        
    def sort_playlist(self, playlist_name):
        playlist = self.search_playlist_by_name(playlist_name)
        if playlist is None:
            print("No such playlist exists in the Music Player.")
            return
        playlist.get_playlist().sort_list()
        return
    
    def play_shuffled_song(self, playlist_name):
        playlist = self.search_playlist_by_name(playlist_name)
        if playlist is None:
            print("No such playlist exists in the Music Player.")
            return
        print(playlist.get_playlist().shuffle_song())
        return
    
    def list_all_playlists(self):
        for playlist in self.playlists:
            print(playlist.playlist_name)
            
    def search_playlist_by_name(self, name):
        for playlist in self.playlists:
            if playlist.playlist_name == name:
                return playlist
            
        return None
    
    def delete_playlist(self, name):
        for playlist in self.playlists:
            if playlist.playlist_name == name:
                del playlist
                return True
        
        return False

def create_linked_list():
    with open('app_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        linked_list = LinkedList()
        for row in reader:
            song = Song(row['Song ID'], row['Song Name'], row['Song Length'])
            listnode = ListNode(song)
            linked_list.insert_at_start(listnode)
            
    return linked_list

if __name__ == "__main__":
    musicplayer = MusicPlayer()
    
    linked_list = create_linked_list()
    
    playlist = PlayList(1, 'Songs', linked_list)
    
    print("\nAdding playlist to the Music Player \n")
    musicplayer.add_playlist(playlist)
    
    print(f'Playing all songs in the playlist : {playlist.playlist_name}: \n')
    musicplayer.play_playlist('Songs')
    
    print(f'\nDeleting the Song with name : Old And Secrets \n')
    musicplayer.delete_song_from_playlist('Songs', 'Old And Secrets')
    musicplayer.play_playlist('Songs')
    
    print('\nPlaying all songs after sorting based on song names: \n')
    musicplayer.sort_playlist('Songs')
    musicplayer.play_playlist('Songs')
    
    print('\nPlaying shuffled song \n')
    musicplayer.play_shuffled_song('Songs')