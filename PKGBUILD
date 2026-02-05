# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>
pkgname=welcome_lts
_pkgname=welcome_lts
pkgver=1
pkgrel=02
pkgdesc="Welcome application for helwanlinux"
arch=('any')
url="https://github.com/helwan-linux/welcome_lts"
license=('GPL3')
conflicts=('helwan-welcome-app')
makedepends=('git')
depends=('python-pyqt5' 'gettext' 'libwnck3' 'arandr')
provides=("${pkgname}")
install='readme.install'
options=(!strip !emptydirs)
source=(${_pkgname}::"git+${url}")
sha256sums=('SKIP')

package() {
    # 1. تثبيت مجلد التطبيق
    install -Dm755 -d "$pkgdir/usr/share/helwan-welcome-app"
    cp -r "${srcdir}/${_pkgname}/usr/share/helwan-welcome-app/"* "$pkgdir/usr/share/helwan-welcome-app/"

    # 2. إنشاء ملف التشغيل لحل مشكلة الـ Import ولعمل اختصار welcome_lts
    install -dm755 "$pkgdir/usr/bin"
    echo -e "#!/bin/bash\ncd /usr/share/helwan-welcome-app/ && python helwan-welcome-app.py \"\$@\"" > "$pkgdir/usr/bin/helwan-welcome-app"
    chmod +755 "$pkgdir/usr/bin/helwan-welcome-app"
    ln -sf /usr/bin/helwan-welcome-app "$pkgdir/usr/bin/welcome_lts"

    # 3. تثبيت ملف الـ .desktop
    install -Dm644 "${srcdir}/${_pkgname}/usr/share/applications/helwan-welcome-app.desktop" "$pkgdir/usr/share/applications/helwan-welcome-app.desktop"

    # 4. تعديل جزء الأيقونات (تثبيت مباشر للمسارات المطلوبة)
    install -dm755 "$pkgdir/usr/share/icons/hicolor/scalable/apps"
    install -dm755 "$pkgdir/usr/share/icons/hicolor/512x512/apps"

    # البحث عن ملفات الأيقونة وتثبيتها بالاسم الصحيح الذي يطلبه ملف الـ .desktop
    find "${srcdir}/${_pkgname}/usr/share/hicolor" -name "helwan-welcom.*" -print0 | while IFS= read -r -d $'\0' file; do
        if [[ "$(basename "$file")" == "helwan-welcom.svg" ]]; then
            install -Dm644 "$file" "$pkgdir/usr/share/icons/hicolor/scalable/apps/helwan-welcome.svg"
        elif [[ "$(basename "$file")" == "helwan-welcom.png" ]]; then
            install -Dm644 "$file" "$pkgdir/usr/share/icons/hicolor/512x512/apps/helwan-welcome.png"
        fi
    done

    # 5. ملفات الترجمة والترخيص
    find "${srcdir}/${_pkgname}/usr/share/helwan-welcome-app/locales" -name "base.mo" -print0 | while IFS= read -r -d $'\0' file; do
        lang_dir=$(basename "$(dirname "$(dirname "$file")")")
        install -Dm644 "$file" "$pkgdir/usr/share/locale/$lang_dir/LC_MESSAGES/base.mo"
    done

    install -dm755 "$pkgdir/usr/share/licenses/${pkgname}"
    install -Dm644 "${srcdir}/${_pkgname}/LICENSE" "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
