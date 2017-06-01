install(FILES csps.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

install (CODE "execute_process (COMMAND pyinstaller --noconfirm \
						--clean \
						--log-level=ERROR \
						--noupx \
						--windowed \
						--onefile \
						--add-binary /System/Library/Frameworks/Tcl.framework/Versions/8.5/Tcl:./build \
						--add-binary /System/Library/Frameworks/Tk.framework/Versions/8.5/Tk:./build \
						csps.py WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})")
