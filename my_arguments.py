def ec2_arguments(parser):
    parser.add_argument("-ec2",
                        "--create_ec2",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-vid", "--vpc_id",
                        required=False)

    parser.add_argument("-sid",
                        "--subnet_id",
                        required=False,
                        nargs="?")
    parser.add_argument("-ssh_my_ip", required=False, default="True", action="store_true")
    parser.add_argument("-sg_id", required=False)
    return parser


def vpc_arguments(parser):
    parser.add_argument("-vpc_id", required=False)
    parser.add_argument("-create_private_subnet", type=str, required=False)

    parser.add_argument("-igw",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-vpc",
                        "--create_vpc",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-priv",
                        "--private_subnets",
                        type=int, nargs="?",
                        required=False)

    parser.add_argument("-pub",
                        "--public_subnets",
                        type=int, nargs="?",
                        required=False)

    return parser


def rds_arguments(parser):
    parser.add_argument("-new_pass", type=str, required=False)

    parser.add_argument("-dbInstanceId", type=str, required=False)

    parser.add_argument("-rds",
                        "--rds_type",
                        required=False,
                        choices=["mysql",
                                 "postgres",
                                 "mariadb",
                                 "aurora-mysql"])

    parser.add_argument("-rds_i",
                        "--rds_identifier",
                        required=False)

    parser.add_argument("-rds_dets",
                        "--get_rds_details",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("--storage_increase",
                        required=False,
                        type=int)

    parser.add_argument("-vid", "--vpc_id",
                        required=False)

    parser.add_argument("-sids",
                        "--multiple_subnet_id",
                        required=False,
                        nargs="*")

    parser.add_argument("-mrds",
                        "--modify_rds",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-snap",
                        "--make_snapshot",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-snapi",
                        "--snap_identifier",
                        required=False)

    return parser


def dynamo_db_arguments(parser):
    parser.add_argument("-ltbs",
                        "--list_tables",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    return parser


def bastion_arguments(parser):
    parser.add_argument("-rds",
                        "--rds_type",
                        required=False,
                        choices=["mysql",
                                 "postgres",
                                 "mariadb",
                                 "aurora-mysql"])

    parser.add_argument("-sids",
                        "--multiple_subnet_id",
                        required=False,
                        nargs="*")

    parser.add_argument("-vid", "--vpc_id",
                        required=False)

    parser.add_argument("-rds_i",
                        "--rds_identifier",
                        required=False)

    parser.add_argument("-ec2",
                        "--create_ec2",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-bastion",
                        "--create_bastion_host",
                        default="False",
                        choices=["True", "False"],
                        required=False)

    parser.add_argument("-sid",
                        "--subnet_id",
                        required=False,
                        nargs="?")
    return parser


def bucket_arguments(parser):
    parser.add_argument("-organize", required=False)
    parser.add_argument("-bn", "--bucket_name", required=False)
    parser.add_argument("-upload_file", type=str, required=False)
    return parser
