#!/bin/sh
# 解锁keychain，以便可以正常的签名应用，
PASSWORD="lyw520,,"
security unlock-keychain -p $PASSWORD ~/Library/Keychains/login.keychain

# 获取设备的UDID
UDID=$(idevice_id -l | head -n1)

cd /Users/xj/code/WebDriverAgent

# 运行测试
xcodebuild -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=$UDID" test