import psycopg2,os,time

def getconn():
    return psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")


def update_job_status(jobid,status,filename):
    conn = getconn()
    cur = conn.cursor()
    finish_date = time.strftime("%Y-%m-%d", time.localtime())
    finish_time = time.strftime("%H:%M:%S", time.localtime())
    sql = "update jobs set job_status = '%s' , outputpath= '%s', finish_date='%s',finish_time='%s'  " \
          "where job_id = %s;" % (str(status), filename,finish_date,finish_time, str(jobid))
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_res_path(medaid):
    conn = getconn()
    cur = conn.cursor()
    sql = "select res_path , file_name from resources where resource_id = %s" % medaid
    cur.execute(sql)
    result = cur.fetchone()
    conn.close()
    path = os.path.join(result[0],result[1])
    return path


# update_job_status(2,1)
#get_res_path(3)





