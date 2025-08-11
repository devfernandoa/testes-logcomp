from compiler_testing_lib.runner import TestRunner
runner = TestRunner(language='C', version='v2.0', max_errors=3, timeout=10, file_extension='c')
result = runner.run_tests(command_template='python3 main.py')
print(result)