{
  "variables": {
    # may be redefined in command line on configuration stage
    # "BUILD_LIBRDKAFKA%": "<!(echo ${BUILD_LIBRDKAFKA:-1})"
    "BUILD_LIBRDKAFKA%": "<!(node ./util/get-env.js BUILD_LIBRDKAFKA 1)",
  },
  "targets": [
    {
      "target_name": "node-librdkafka",
      'sources': [
        'src/binding.cc',
        'src/callbacks.cc',
        'src/common.cc',
        'src/config.cc',
        'src/connection.cc',
        'src/errors.cc',
        'src/kafka-consumer.cc',
        'src/producer.cc',
        'src/topic.cc',
        'src/workers.cc'
      ],
      "include_dirs": [
        "<!(node -e \"require('nan')\")",
        "<(module_root_dir)/"
      ],
      'conditions': [
        [
          'OS=="win"',
          {
            'cflags_cc' : [
              '-std=c++11'
            ],
            'msvs_settings': {
              'VCCLCompilerTool': {
                'AdditionalOptions': [
                  '/GR'
                ],
                'AdditionalUsingDirectories': [
                  '<(module_root_dir)/deps/librdkafka/win32/outdir/v120/x64/Release/'
                ]
              }
            },
            'msvs_version': '2013',
            'msbuild_toolset': 'v120',
            "dependencies": [
              "<(module_root_dir)/deps/librdkafka.gyp:librdkafka"
            ],
            'include_dirs': [
              'deps/librdkafka/src-cpp'
            ]
          },
          {
            # Still not fully clear why I need to do this
            # These should have been done in the librdkafka makefile
            'conditions': [
              [ "<(BUILD_LIBRDKAFKA)==1",
                {
                  "dependencies": [
                    "<(module_root_dir)/deps/librdkafka.gyp:librdkafka"
                  ],
                  "include_dirs": [
                    "deps/librdkafka/src-cpp"
                  ],
                  'conditions': [
                    [
                      'OS=="linux"',
                      {
                        "libraries": [
                          "-L<(module_root_dir)/build/Release",
                          "-lrdkafka++",
                          "-lrdkafka",
                          "-Wl,-rpath=<(module_root_dir)/build/Release",
                        ],
                      }
                    ],
                    [
                      'OS=="mac"',
                      {
                        "libraries": [
                          "<(module_root_dir)/build/Release/librdkafka++.dylib",
                          "<(module_root_dir)/build/Release/librdkafka.dylib",
                        ],
                      }
                    ]
                  ],
                },
                # Else link against globally installed rdkafka and use
                # globally installed headers.  On Debian, you should
                # install the librdkafka1, librdkafka++1, and librdkafka-dev
                # .deb packages.
                {
                  "libraries": ["-lrdkafka", "-lrdkafka++"],
                  "include_dirs": [
                    "/usr/include/librdkafka",
                    "/usr/local/include/librdkafka"
                  ],
                },
              ],
              [
                'OS=="linux"',
                {
                  'cflags_cc' : [
                    '-std=c++11'
                  ],
                  'cflags_cc!': [
                    '-fno-rtti'
                  ]
                }
              ],
              [
                'OS=="mac"',
                {
                  'xcode_settings': {
                    'MACOSX_DEPLOYMENT_TARGET': '10.11',
                    'GCC_ENABLE_CPP_RTTI': 'YES',
                    'OTHER_CPLUSPLUSFLAGS': [
                      '-std=c++11'
                    ],
                  },
                }
              ]
            ]
          }
        ]
      ]
    }
  ]
}