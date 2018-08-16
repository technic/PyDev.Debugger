import os

import pytest

from tests_python import debugger_unittest
from tests_python.debugger_unittest import IS_IRONPYTHON, IS_JYTHON, overrides, builtin_qualifier

pytest_plugins = [
    str('tests_python.debugger_fixtures'),
]


@pytest.mark.skipif(IS_IRONPYTHON or IS_JYTHON, reason='Failing on IronPython and Jython (needs to be investigated).')
def test_case_type_ext(case_setup):
    # Custom type presentation extensions

    def get_environ(self):
        env = os.environ.copy()

        python_path = env.get("PYTHONPATH", "")
        ext_base = debugger_unittest._get_debugger_test_file('my_extensions')
        env['PYTHONPATH'] = ext_base + os.pathsep + python_path  if python_path else ext_base
        return env

    with case_setup.test_file('_debugger_case_type_ext.py', get_environ=get_environ) as writer:
        writer.get_environ = get_environ

        writer.write_add_breakpoint(7, None)
        writer.write_make_initial_run()

        hit = writer.wait_for_breakpoint_hit('111')
        writer.write_get_frame(hit.thread_id, hit.frame_id)
        assert writer.wait_for_var([
            [
                r'<var name="my_rect" type="Rect" qualifier="__main__" value="Rectangle%255BLength%253A 5%252C Width%253A 10 %252C Area%253A 50%255D" isContainer="True" />',
                r'<var name="my_rect" type="Rect"  value="Rect: <__main__.Rect object at',  # Jython
            ]
        ])
        writer.write_get_variable(hit.thread_id, hit.frame_id, 'my_rect')
        assert writer.wait_for_var(r'<var name="area" type="int" qualifier="{0}" value="int%253A 50" />'.format(builtin_qualifier))
        writer.write_run_thread(hit.thread_id)
        writer.finished_ok = True


@pytest.mark.skipif(IS_IRONPYTHON or IS_JYTHON, reason='Failing on IronPython and Jython (needs to be investigated).')
def test_case_event_ext(case_setup):

    def get_environ(self):
        env = os.environ.copy()

        python_path = env.get("PYTHONPATH", "")
        ext_base = debugger_unittest._get_debugger_test_file('my_extensions')
        env['PYTHONPATH'] = ext_base + os.pathsep + python_path  if python_path else ext_base
        env["VERIFY_EVENT_TEST"] = "1"
        return env

    # Test initialize event for extensions
    with case_setup.test_file('_debugger_case_event_ext.py', get_environ=get_environ) as writer:

        original_additional_output_checks = writer.additional_output_checks

        @overrides(writer.additional_output_checks)
        def additional_output_checks(stdout, stderr):
            original_additional_output_checks(stdout, stderr)
            if 'INITIALIZE EVENT RECEIVED' not in stdout:
                raise AssertionError('No initialize event received')

        writer.additional_output_checks = additional_output_checks

        writer.write_make_initial_run()
        writer.finished_ok = True

