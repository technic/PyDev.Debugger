import sys, os.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'site-packages'))
                
import file_on_site_packages


def step_over_my_code():
    x = 2
    return x  # break here


if __name__ == '__main__':
    for _ in range(2):
        x = file_on_site_packages.call_my_code(step_over_my_code)
        assert x == 2

    print('TEST SUCEEDED')
