import sqlite3
import os

class Database:
    db_name = "auth.db"
    def __init__(self,keep_connected=True):
        self.connected = keep_connected
        if not os.path.exists(self.db_name):
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.createTables()
            if not self.connected:
                self.close()
                
                
        elif self.connected:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            
            
    def createTables(self):
        user_table = """
        CREATE TABLE users(
            id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
        
        session_table="""
            CREATE TABLE sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        
        try:
            self.cursor.execute(user_table)
            self.cursor.execute(session_table)
            self.conn.commit()
            
        except Exception as e:
            print("Database Error:",e)
            self.conn.rollback()
        except:
            print("While Creating Table Something Went Wrong")
            self.conn.rollback()        
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def execute(self,query,data):
        if not self.connected:
            self.connect()
            
        execution = False
            
        try:
            self.cursor.execute(query,data)
            self.conn.commit()
            execution = True
        except Exception as e:
            print("Database Error:",e)
            self.conn.rollback()
        except:
            print("Query Execution Failed")
            self.conn.rollback() 
            
        return (execution,self.cursor.fetchall())
            
            
        
    def newUser(self,username,password_hash,email):
        query = """
        INSERT INTO users (username,email,password_hash) VALUES (?,?,?)
        """
        data = (username,email,password_hash)
        
        return self.execute(query,data)[0]
    
    
    def nameHash(self,username):
        query = """
        SELECT username,password_hash,id FROM users WHERE username=?
        """
        
        data = (username,)
        
        return self.execute(query,data)
    
    def emailHash(self,email):
        query = """
        SELECT email,password_hash,id FROM users WHERE email=?
        """
        
        data = (email,)
        
        return self.execute(query,data)
    
    def createSession(self,user_id,session_id):
        query = """
        INSERT INTO sessions (session_id,user_id) VALUES (?,?)
        """
        data = (session_id,user_id)
        
        
        return self.execute(query,data)[0]
    
    def retriveSession(self,session_id):
        query = """
        SELECT user_id,created_at FROM sessions WHERE session_id=?
        """
        
        data = (session_id,)
        
        return self.execute(query,data)
    
    def updateInteraction(self,session_id):
        query = """
        UPDATE sessions SET last_interaction = CURRENT_TIMESTAMP WHERE session_id=?
        """
        
        data = (session_id,)
        
        return self.execute(query,data)[0]
          
    def removeSession(self,session_id):
        query = """
        DELETE FROM sessions WHERE session_id=?
        """
        
        data = (session_id,)
        
        return self.execute(query,data)
    
    def countEmail(self,email):
        query = "SELECT COUNT(*)  FROM users WHERE email = ? " 
        
        data = (email,)
        print(self.execute(query,data))
        return self.execute(query,data)
    
    def countName(self,name):
        query = "SELECT COUNT(*)  FROM users WHERE username = ? " 
        
        data = (name,)
        return self.execute(query,data)

        
    
    def duplicateSessionName(self,name):
        query = "SELECT id,password_hash  FROM users WHERE username = ? " 
        
        data = (name,)
        
        user_data = self.execute(query,data)
        
        if(len(user_data)==0):
            return (False,[])
        
        user_id = user_data[0]
        
        query = "SELECT session_id,created_at FROM sessions WHERE user_id = ?"
        
        session_data = self.execute(query,(user_id,))
        
        if(session_data[0] and len(session_data[1])>0):
            return (True,[name,user_data[1][0][1],user_id,session_data[0]])
        
        else:
            return (False,[name,user_data[1][0][1],user_id])
        
        
    def duplicateSessionEmail(self,email):
        query = "SELECT id,password_hash  FROM users WHERE email = ? " 
        
        data = (email,)
        
        user_data = self.execute(query,data)
        
        if(len(user_data)==0):
            return (False,[])
        
        user_id = user_data[0]
        
        query = "SELECT session_id,created_at FROM sessions WHERE user_id = ?"
        
        session_data = self.execute(query,(user_id,))
        
        if(session_data[0] and len(session_data[1])>0):
            return (True,[email,user_data[1][0][1],user_id,session_data[0]])
        
        else:
            return (False,[email,user_data[1][0][1],user_id])
            
        
        
        
        
        
        
        
        