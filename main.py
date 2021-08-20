from shutil import disk_usage,move,make_archive,rmtree
import pathlib as pl
import datetime
from os import  makedirs

total, used, free = disk_usage('/')
ten_per =  free/total * 100 * 10

def cleaner(def_dir='test_archive'):
    for dir in pl.Path(def_dir).iterdir():
        try:
            if dir.is_dir():
                dir.rmdir()
        except:
            cleaner(dir)
    return 'CLEAR'

def to_zip(path:pl.Path):
    root = str(path.parent).split('/')[:]
    root[0] = 'test_archive'
    root = pl.Path('/'.join(root))

    make_archive('-'.join(str(path).split('/')[1:]),'zip', root_dir=root)
    move(str(list(pl.Path('.').glob('*.zip'))[0]), 'test_archive')
    rmtree(root, ignore_errors=True)
    cleaner()
    f.write(f"Zip archive = {'-'.join(str(path).split('/')[1:])} was created \n")

def to_archive(path:pl.Path):
    from_path = path
    to_path =  '/'.join(str(from_path).split('/')[1:])
    to_path = pl.Path(str('test_archive/'+to_path))
    try:
        makedirs(to_path.parent.absolute())
    except:
        pass
    move(from_path,to_path)

f = open('log.txt','w')

start_path = pl.Path('test_storage')
IS_ARCHIVED = False
while True:
    for year in [x for x in start_path.iterdir() if x.is_dir()]:
        start_year = pl.Path(year)
        for month in [x for x in start_year.iterdir() if x.is_dir()]:
            start_year_month = pl.Path(month)
            for day in [x for x in start_year_month.iterdir() if x.is_dir()]:
                start_year_month_day = pl.Path(day)
                print([x for x in start_year_month_day.iterdir()])
                for record in [x for x in start_year_month_day.iterdir()]:
                    print("HERE IS A RECORD")
                    start_year_month_day_record = pl.Path(record)
                    parent = start_year_month_day_record.parent
                    s = '/'.join(str(parent).split('/')[1:])
                    date_to_check = datetime.datetime.strptime(s,'%Y/%m/%d')
                    date_now = datetime.datetime.today()


                    if (date_now-date_to_check).days > 90:
                        f.write(f'Found file older than 90 days. File is {start_year_month_day_record}. Archiving starts.\n')
                        to_archive(start_year_month_day_record)
                        IS_ARCHIVED = True

                    else:
                        total, used, free = disk_usage('/')
                        ten_per = free / total * 100 * 10
                        if free < ten_per:
                            f.write(f'Storage is overloaded. Start to archiving file = {start_year_month_day_record}\n')
                            to_archive(start_year_month_day_record)
                            IS_ARCHIVED = True

                if IS_ARCHIVED:
                    to_zip(start_year_month_day)
                    IS_ARCHIVED = False
    cleaner('test_storage')


