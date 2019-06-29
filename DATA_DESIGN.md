# DATA DESIGN

### product

- product_id (pk)
- name
- category_id (fk)
- price

### category

- category_id (pk)
- name

### build

- build_id (pk)
- name

### build_product

- build_product_id (pk)
- build_id (fk)
- product_id (fk)
- status_cd