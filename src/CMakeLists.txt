install(FILES python_gui_test.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
install(CODE "execute_process(COMMAND pyinstaller -w python_gui_test.py WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})")