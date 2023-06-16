## EC2 script         

### Tips:
install certifi     
        
    pip install certifi     #for retrieving your ip with certification(avoid error)

### Allows creating:

VPC,    
Internet gateway for VPC,   
Desired amount of private and public subnets.

    
### Launch vpc with:
#### Created security group with:    
ssh access only from host machine(on which this script will run)
gives access to http requests from any ip   

creates and downloads .pem key

### command examples:    
To create vpc:

    python main.py vpc -vpc True -igw True -pub 3 -priv 3
to launch ec2 instance:
    
    python main.py ec2 -ec2 True -sid subnet-0321f7038406c24cd -vid vpc-038a43744418c24d7


### arguments:
        
        -vpc True //to create vpc (takes only True or False arguments)

        -igw True //for script to create internet gateway and atttach it to vpc (takes only True or False arguments)

        -pub/--public_subnets X(number of subnets) //to pass amount of public subnets to create with vpc

        -priv/--private_subnets X(number of subnets) //to pass amount of private subnets to create with vpc

        -vid/--vpc_id //pass vpc id to which you want operation on e.g. launch instance

        -sid/--subnet_id //pass subnet id to which we want operation on e.g launch instance

there's time.sleep() function used to slow down creating subnets. Otherways it gives errors

# RDS
## launching RDS

command example:    

    python main.py rds -vid vpc-081b5d31efb75b7f7 --rds_type mysql -rds_i mysql1818-btu -sids subnet-067ffb82773cac341 subnet-01e3488b70076ea46


### Arguments for launching RDS:
    
    -rds_i/--rds_identifier //takes unique name for RDS database

    -rds/--rds_type //to pass what type of rds do you want made. takes only["mysql", "postgres", "mariadb", "aurora-mysql"]. currently working only for mysql
    
    -vid/--vpc_id //pass vpc id to which we create RDS on

    -sids/--multiple_subnet_id //subnets to where RDS database will be setup. requires passing of at least 2 different AZ subnets

## Getting RDS details

command example:

     python main.py rds -rds_dets True -rds_i mysql1818-btu 

### Arguments for getting RDS details:

    -rds_dets/--rds_details //takes only ["True","False"] arguments. if true, returns details
    -rds_i/--rds_identifier //takes database's unique identifier to return details of
    
## Increase RDS Storage

    python main.py rds --storage_increase 20 --rds_identifier mysql1818-btu --modify_rds True

### Arguments for Increasing RDS Storage

    --storage_increase #how many gigs of storage to add
    --rds_identifier #which database are we changing
    --modify_rds True #indicate that you want database changed

## RDS Backups
command example:

    python main.py rds --snap_identifier mysnap2 --rds_identifier mysql1818-btu --make_snapshot True 

### Arguments

    -snapi/--snap_identifier    #unique name for snapshot
    -rds_i/--rds_identifier     #name of database to backup
    -snap/--make_snapshot       #to be sure you want snapshot made


# DynamoDB
### List all tables in current region:
    
    python main.py dynamo_db -ltbs True

### Arguments:
    
    -ltbs/--list_tables #lists all tables in current region chosen in .env
.........