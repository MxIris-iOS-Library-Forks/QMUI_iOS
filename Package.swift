// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "QMUIKit",
    products: [
        // Products define the executables and libraries a package produces, making them visible to other packages.
        .library(
            name: "QMUIKit",
            targets: ["QMUIKit"]
        ),
    ],
    targets: [
        // Targets are the basic building blocks of a package, defining a module or a test suite.
        // Targets can depend on other targets in this package and products from dependencies.
        .target(
            name: "QMUIKit",
            path: "QMUIKit",
            cSettings: [
                .headerSearchPath("./QMUICore"),
                .headerSearchPath("./QMUIComponents"),
                .headerSearchPath("./QMUIComponents/AssetLibrary"),
                .headerSearchPath("./QMUIComponents/ImagePickerLibrary"),
                .headerSearchPath("./QMUIComponents/NavigationBarTransition"),
                .headerSearchPath("./QMUIComponents/QMUIAnimation"),
                .headerSearchPath("./QMUIComponents/QMUIBadge"),
                .headerSearchPath("./QMUIComponents/QMUIButton"),
                .headerSearchPath("./QMUIComponents/QMUICellHeightKeyCache"),
                .headerSearchPath("./QMUIComponents/QMUICellSizeKeyCache"),
                .headerSearchPath("./QMUIComponents/QMUIConsole"),
                .headerSearchPath("./QMUIComponents/QMUIImagePreviewView"),
                .headerSearchPath("./QMUIComponents/QMUILog"),
                .headerSearchPath("./QMUIComponents/QMUIMultipleDelegates"),
                .headerSearchPath("./QMUIComponents/QMUIPopupMenuView"),
                .headerSearchPath("./QMUIComponents/QMUIScrollAnimator"),
                .headerSearchPath("./QMUIComponents/QMUITheme"),
                .headerSearchPath("./QMUIComponents/StaticTableView"),
                .headerSearchPath("./QMUIComponents/ToastView"),
                .headerSearchPath("./QMUIMainFrame"),
                .headerSearchPath("./QMUIResources"),
                .headerSearchPath("./UIKitExtensions"),
                .headerSearchPath("./UIKitExtensions/QMUIBarProtocol"),
            ]
        ),
    ]
)
