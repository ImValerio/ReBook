import { MatPaginatorIntl } from '@angular/material/paginator';
export class PersonalizeMatPaginatorIntl extends MatPaginatorIntl {

  override getRangeLabel = (page: number, pageSize: number, length: number): string => {
    if (length === 0 || pageSize === 0) {
      return '';
    }
    return 'page ' + (page + 1) + ' of ' + pageSize;
  };

}