arguments:
        
        -vpc  //to create vpc
        -igw  //for script to create internet gateway and atttach it to vpc
        -pub/--public_subnets  //to pass amount of public subnets
        -priv/--private_subnets  //to pass amount of private subnets

there's time.sleep() function used to slow down creating subnets otherways it gives errors 