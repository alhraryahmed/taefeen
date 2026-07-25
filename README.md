# hajj_umrah_manager
### نظام إدارة الحج والعمرة — شركة الطائفين لخدمات الحج والعمرة

تطبيق Frappe/ERPNext (v14 / v15) خفيف ومباشر لمتابعة المعتمرين، الرحلات، الحجوزات، الأقساط، وخزينة الشركة.

---

## 1. محتوى التطبيق

| DocType | النوع | الوصف |
|---|---|---|
| **Pilgrim** (المعتمر) | Master | بيانات المعتمر، التسجيل الفردي/العائلي، الوثائق |
| **Umrah Trip** (الرحلة/الفوج) | Transactional | رحلة تجمع عدة معتمرين بتاريخ سفر/عودة وملخص مالي تلقائي |
| **Umrah Booking** (حجز عمرة) | Transactional (Submittable) | تكلفة كل معتمر، السعر، الربح، والأقساط |
| **Company Treasury** (الخزينة) | Single | الرصيد الحقيقي للشركة |
| **Treasury Transaction** (حركة الخزينة) | Transactional (Submittable) | إيرادات/مصاريف يدوية أو تلقائية من الحجوزات |

الجداول الفرعية: `Pilgrim Document`, `Family Member`, `Installment Schedule Row`.

---

## 2. التثبيت

على سيرفر يحتوي bench مُهيّأ مسبقاً لـ ERPNext v14/v15:

```bash
# فك الضغط عن الملف داخل مجلد apps الخاص بالـ bench، أو استخدم git إن رفعته إلى مستودع
cd ~/frappe-bench
cp -r /path/to/hajj_umrah_manager apps/

# تثبيت التطبيق كحزمة بايثون داخل بيئة bench
./env/bin/pip install -e apps/hajj_umrah_manager

# ربط التطبيق بالموقع وتفعيله
bench --site your-site.local install-app hajj_umrah_manager
bench --site your-site.local migrate
bench build
bench restart
```

> ملاحظة: عند أول تشغيل لـ `install-app` سيتم تلقائياً إنشاء الدور `Hajj Umrah Manager` (من ملف fixtures)، ويمكنك تعيينه لموظفي الشركة بدل صلاحيات System Manager الكاملة.

---

## 3. تفعيل بلوك الداشبورد (الأخضر والذهبي)

1. من القائمة الجانبية اذهب إلى **Workspace** الخاص بموديول "Hajj and Umrah" (أو أنشئ Workspace جديد باسم "شركة الطائفين").
2. اضغط **Edit** ثم أضف عنصر **Custom Block / HTML Block**.
3. افتح الملف `hajj_umrah_manager/templates/pages/dashboard_block.html` وانسخ محتواه بالكامل والصقه داخل العنصر.
4. احفظ. البلوك يجلب بياناته الحيّة تلقائياً من `hajj_umrah_manager.api.get_dashboard_stats`.

الثيم (الألوان والتنسيق) محمّل تلقائياً مع التطبيق عبر `public/css/hajj_umrah_dashboard.css`.

---

## 4. منطق العمل الأساسي (مُطبّق بالفعل داخل الأكواد)

- **حجز عمرة (Umrah Booking):**
  - `total_expenses` = مجموع (تأشيرة + تذكرة + سكن مكة + سكن المدينة + نقل) — تلقائي.
  - `total_profit` = `umrah_price` − `total_expenses` — تلقائي.
  - `balance_amount` = `umrah_price` − `total_paid` — تلقائي.
  - عند اختيار **Installments** يتم توليد جدول 10 أشهر تلقائياً (القيمة الشهرية = السعر ÷ 10)، ويتحدّث `total_paid` وحالة كل قسط تلقائياً حسب المبلغ المُدخل.
  - عند اختيار **Cash** يظهر زر "تسجيل دفعة كاش" لتسجيل المبلغ المستلم دفعة واحدة أو على دفعات.
  - أي زيادة في `total_paid` تُنشئ تلقائياً **حركة خزينة (Income)** مرتبطة بالحجز، وتُعتمد تلقائياً لتحديث رصيد الخزينة الحقيقي.

- **الخزينة (Company Treasury):** رصيد واحد فعلي يتحدّث تلقائياً من:
  - دفعات المعتمرين (تلقائياً من الحجوزات).
  - أي مصروف يدوي تُسجّله عبر **Treasury Transaction** (نوع Expense) وتعتمده.

- **الرحلة (Umrah Trip):** تُجمّع تلقائياً عدد المعتمرين، إجمالي المصاريف، الإيرادات، والأرباح من كل الحجوزات المرتبطة بها، بدون أي إدخال يدوي.

---

## 5. خارطة طريق (غير مُنفّذة الآن، حسب طلبكم)

- ربط `Umrah Booking` و`Treasury Transaction` بمحاسبة ERPNext الفعلية (Sales Invoice / Payment Entry / Chart of Accounts) بدل النظام المستقل الحالي، عند الحاجة للتقارير المحاسبية الرسمية والإقرارات الضريبية.

---

## 6. الصلاحيات

تم إنشاء دور `Hajj Umrah Manager` بصلاحيات كاملة على DocTypes التطبيق (بدون وصول لإعدادات النظام العامة). عدّل الصلاحيات من **Role Permissions Manager** حسب هيكلة الشركة (مثال: موظف استقبال يرى فقط، محاسب يُدخل حركات الخزينة، مدير يعتمد الحجوزات).
