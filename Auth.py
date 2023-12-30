import Database
import bcrypt
import uuid
import jwt
import datetime




class Auth:
    def __init__(self,inf=True):
        self.db = Database.Database(keep_connected=inf)
        self.secret_key = ""
    
    def hashPassword(self,password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def verifyPassword(self,recived_passord,stored_password):
        return bcrypt.checkpw(recived_passord.encode('utf-8'), stored_password)
      
    
    
    def emailUnique(self,email):
        return self.db.countEmail(email)[1][0]>0
    
    def nameUnique(self,name):
        return self.db.countName(name)[1][0]>0
      
    def registerUser(self,username,email,password):
        if not self.nameUnique(username):
            return (False,{"message":"Duplicate username"})
        
        if not self.emailUnique(email):
            return (False,{"message":"Duplicate email"})
            
            
        res = self.db.newUser(username,self.hash_password(password),email)
        if (res[0]):
            return (True,{"message":"Registration Success"})
        return (False,{"message":"Failed"})
    
    def generateSessionToken(self,session_id,data):
        payload = {
            'extra':data,
            'session_id':session_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        return (True,{"message":"Login Successfull","token":token})
    
    def loginUserEmail(self,email,password,extra_payload = {}):
        loginRes = self.db.emailHash(email)
        if loginRes[0] and len(loginRes[1])>0:
            if self.verifyPassword(password,loginRes[1][1]):
                session_id =  str(uuid.uuid4())
                sessionRes = self.db.createSession(loginRes[1][2],session_id)
                if(sessionRes[0]):
                    return self.generateSessionToken(session_id,extra_payload)
                return (False,{'message':"Unable to create a Session"})
            else:
                return (False,{"message":"Password Didnt Match"})
            
        return (False,{'message':"Invalid Credentials"})
            
            
    def loginUserName(self,name,password,extra_payload):
        loginRes = self.db.nameHash(name)
        if loginRes[0] and len(loginRes[1])>0:
            if self.verifyPassword(password,loginRes[1][1]):
                session_id =  str(uuid.uuid4())
                sessionRes = self.db.createSession(loginRes[1][2],session_id)
                if(sessionRes[0]):
                    return self.generateSessionToken(session_id,extra_payload)
                return (False,{'message':"Unable to create a Session"})
            else:
                return (False,{"message":"Password Didnt Match"})
            
        return (False,{'message':"Invalid Credentials"})
    
    def decodeToken(self,token):
        return jwt.decode(token, self.secret_key, algorithms=['HS256'])
    
    def validateSession(self):
        pass
    
    
    def verifyToken(self,token):
        data = self.decodeToken(token)
        
        session_id =  data.session_id
        
        sessionRes = self.db.retriveSession(session_id)
        
        if sessionRes[0]:
            if self.validateSession():
                self.db.updateInteraction(session_id)
                return (True,{"message":"Valid","data":data})
            else:
                self.db.removeSession(session_id)
                return (False,{"message":"Session Expired"})
        return (False,{"message":"Invalid Token"})
    
    def logoutSession(self,token):
        data = self.decodeToken(token)
        session_id =  data.session_id
        sessionRes = self.db.removeSession(session_id)
        if sessionRes[0]:
            return (True,{"message":"Logged Out"})
        else:
            return (False,{"message":"Session has already logged out"})
    
    
if __name__=="__main__":
    pass