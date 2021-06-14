#!/bin/bash
import xuatools

# @TODO sina implement using argparse

print(xuatools.config.data)
xuatools.config.init()
print(xuatools.config.data)
# print(xuatools.config.clean())
# print(xuatools.config.call())
print(xuatools.build.general('server_php', 'some_shit.xua'))

print(xuatools.compiler.server_php_codegen('source code'))
