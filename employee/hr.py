# -*- coding: utf-8 -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/

from sqlalchemy import *
from sqlalchemy.databases.oracle import *

metadata = MetaData()


regions =  Table('regions', metadata,
    Column(u'region_id', Numeric(asdecimal=False), primary_key=True, nullable=False),
            Column(u'region_name', VARCHAR(length=25), primary_key=False),
    
    schema='HR'
    )


countries =  Table('countries', metadata,
    Column(u'country_id', CHAR(length=2), primary_key=True, nullable=False),
            Column(u'country_name', VARCHAR(length=40), primary_key=False),
            Column(u'region_id', Numeric(asdecimal=False), primary_key=False),
    ForeignKeyConstraint([u'region_id'], [u'hr.regions.region_id'], name=u'COUNTR_REG_FK'),
    schema='HR'
    )


locations =  Table('locations', metadata,
    Column(u'location_id', Numeric(precision=4, scale=0, asdecimal=False), primary_key=True, nullable=False),
            Column(u'street_address', VARCHAR(length=40), primary_key=False),
            Column(u'postal_code', VARCHAR(length=12), primary_key=False),
            Column(u'city', VARCHAR(length=30), primary_key=False, nullable=False),
            Column(u'state_province', VARCHAR(length=25), primary_key=False),
            Column(u'country_id', CHAR(length=2), primary_key=False),
    ForeignKeyConstraint([u'country_id'], [u'hr.countries.country_id'], name=u'LOC_C_ID_FK'),
    schema='HR'
    )
Index(u'loc_city_ix', locations.c.city, unique=False)
Index(u'loc_country_ix', locations.c.country_id, unique=False)
Index(u'loc_state_province_ix', locations.c.state_province, unique=False)


departments =  Table('departments', metadata,
    Column(u'department_id', Numeric(precision=4, scale=0, asdecimal=False), primary_key=True, nullable=False),
            Column(u'department_name', VARCHAR(length=30), primary_key=False, nullable=False),
            Column(u'manager_id', Numeric(precision=6, scale=0, asdecimal=False), primary_key=False),
            Column(u'location_id', Numeric(precision=4, scale=0, asdecimal=False), primary_key=False),
    ForeignKeyConstraint([u'manager_id'], [u'hr.employees.employee_id'], name=u'DEPT_MGR_FK'),
            ForeignKeyConstraint([u'location_id'], [u'hr.locations.location_id'], name=u'DEPT_LOC_FK'),
    schema='HR'
    )
Index(u'dept_location_ix', departments.c.location_id, unique=False)


jobs =  Table('jobs', metadata,
    Column(u'job_id', VARCHAR(length=10), primary_key=True, nullable=False),
            Column(u'job_title', VARCHAR(length=35), primary_key=False, nullable=False),
            Column(u'min_salary', Numeric(precision=6, scale=0, asdecimal=False), primary_key=False),
            Column(u'max_salary', Numeric(precision=6, scale=0, asdecimal=False), primary_key=False),
    
    schema='HR'
    )


employees =  Table('employees', metadata,
    Column(u'employee_id', Numeric(precision=6, scale=0, asdecimal=False), primary_key=True, nullable=False),
            Column(u'first_name', VARCHAR(length=20), primary_key=False),
            Column(u'last_name', VARCHAR(length=25), primary_key=False, nullable=False),
            Column(u'email', VARCHAR(length=25), primary_key=False, nullable=False),
            Column(u'phone_number', VARCHAR(length=20), primary_key=False),
            Column(u'hire_date', DATE(), primary_key=False, nullable=False),
            Column(u'job_id', VARCHAR(length=10), primary_key=False, nullable=False),
            Column(u'salary', Numeric(precision=8, scale=2), primary_key=False),
            Column(u'commission_pct', Numeric(precision=2, scale=2), primary_key=False),
            Column(u'manager_id', Numeric(precision=6, scale=0, asdecimal=False), primary_key=False),
            Column(u'department_id', Numeric(precision=4, scale=0, asdecimal=False), primary_key=False),
    ForeignKeyConstraint([u'job_id'], [u'hr.jobs.job_id'], name=u'EMP_JOB_FK'),
            ForeignKeyConstraint([u'department_id'], [u'hr.departments.department_id'], name=u'EMP_DEPT_FK'),
            ForeignKeyConstraint([u'manager_id'], [u'hr.employees.employee_id'], name=u'EMP_MANAGER_FK'),
    schema='HR'
    )
Index(u'emp_job_ix', employees.c.job_id, unique=False)
Index(u'emp_email_uk', employees.c.email, unique=True)
Index(u'emp_name_ix', employees.c.last_name, employees.c.first_name, unique=False)
Index(u'emp_manager_ix', employees.c.manager_id, unique=False)
Index(u'emp_department_ix', employees.c.department_id, unique=False)


job_history =  Table('job_history', metadata,
    Column(u'employee_id', Numeric(precision=6, scale=0, asdecimal=False), primary_key=True, nullable=False),
            Column(u'start_date', DATE(), primary_key=True, nullable=False),
            Column(u'end_date', DATE(), primary_key=False, nullable=False),
            Column(u'job_id', VARCHAR(length=10), primary_key=False, nullable=False),
            Column(u'department_id', Numeric(precision=4, scale=0, asdecimal=False), primary_key=False),
    ForeignKeyConstraint([u'employee_id'], [u'hr.employees.employee_id'], name=u'JHIST_EMP_FK'),
            ForeignKeyConstraint([u'job_id'], [u'hr.jobs.job_id'], name=u'JHIST_JOB_FK'),
            ForeignKeyConstraint([u'department_id'], [u'hr.departments.department_id'], name=u'JHIST_DEPT_FK'),
    schema='HR'
    )
Index(u'jhist_employee_ix', job_history.c.employee_id, unique=False)
Index(u'jhist_job_ix', job_history.c.job_id, unique=False)
Index(u'jhist_department_ix', job_history.c.department_id, unique=False)

