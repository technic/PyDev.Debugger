pytest_plugins = [
    str('tests_python.debugger_fixtures'),
]


def test_case_get_frames_json(case_setup):
    # Custom type presentation extensions

    with case_setup.test_file('_debugger_case_json_msgs.py') as writer:
        #: :type writer AbstractWriterThread:
        writer.write_make_initial_run()

        hit = writer.wait_for_breakpoint_hit('105')
        
        writer.write_get_variables_json(hit.thread_id, hit.frame_id)
        
        writer.wait_for_message(lambda msg:False)
        
        writer.write_run_thread(hit.thread_id)
        writer.finished_ok = True