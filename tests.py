from functions.get_files_info import get_files_info

def test_calc_dot():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)

def test_calc_pkg():
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

def test_calc_bin():
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

def test_calc_dotdotslash():
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)

test_calc_dot()
test_calc_pkg()
test_calc_bin()
test_calc_dotdotslash()