from sqlalchemy import create_engine,text, bindparam
import bcrypt
db_connection_string="mysql+pymysql://lsx2tv1ao9xih3tjeic2:pscale_pw_1MN7T7O4ErQFuFpdv1lX89OXpiIZctf7bi4F6bMRwOb@aws.connect.psdb.cloud/selvacareers?charset=utf8mb4"

engine = create_engine(
    db_connection_string, 
    connect_args={
        'ssl': {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })

def login_from_db(name, password):
    with engine.connect() as conn:
        query = text('SELECT * FROM register WHERE name = :name')
        params = {'name': name}
        result = conn.execute(query, params)
        user_data = result.fetchone()
        if user_data is not None:
            stored_password_hash = user_data[2] 
            provided_password_str = str(password)  
            if bcrypt.checkpw(provided_password_str.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return user_data
    return None

def register_to_db(data):
        with engine.connect() as conn:
            
            query = text(  
                "INSERT INTO register(name,password,address, contact, mail) "
                "VALUES (:name,:password,:address,:contact, :mail)"
            )
            params = {
                'name': data['name'],
                'password':data['password'],
                'address': data['address'],
                'contact': data['contact'],
                'mail': data['mail']
                
            }
            conn.execute(query, params)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text('select*from jobs'))
        rows = result.fetchall()
        jobs =[]
    for row in rows:
        row = row._asdict()
        jobs.append(row)
    return jobs
        
        
def load_job_from_db(id):
    with engine.connect() as conn:
        query = text('SELECT * FROM jobs WHERE id = :val').bindparams(val=id)
        result = conn.execute(query)
        rows = result.fetchall()
        
        if len(rows) == 0:
            return None
        
        jobs = [row._asdict() for row in rows]
        return jobs
    
        
def add_application_to_db(data,job_id):
    with engine.connect() as conn:
        query = text( 
            "INSERT INTO applications(job_id,full_name, email, linkedin_url, education, work_experience, resume_url) "
            "VALUES (:job_id,:full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
        )
        # Define bind parameters
        params = {
            'job_id': job_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'linkedin_url': data['linkedin_url'],
            'education': data['education'],
            'work_experience': data['work_experience'],
            'resume_url': data['resume_url']
        }
        conn.execute(query, params)