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

- build_id (pk) (fk)
- product_id (pk) (fk)
- status_cd