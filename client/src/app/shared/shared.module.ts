import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatInputModule} from '@angular/material/input';

import {InputSearchComponent} from './input-search/input-search.component';
import {PageBodyComponent} from './layout/page-body/page-body.component';
import {PageHeaderComponent} from './layout/page-header/page-header.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { ListService } from './list.service';
import {MatPaginatorIntl, MatPaginatorModule} from '@angular/material/paginator';
import { PersonalizeMatPaginatorIntl } from './PersonalizeMatPaginatorIntl';

@NgModule({
  declarations: [
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
  ],
  exports:[
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
    MatAutocompleteModule,
    MatInputModule,
    MatPaginatorModule
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatInputModule,
    MatAutocompleteModule,
    MatPaginatorModule
  ],
  providers: [
    ListService,
    { provide: MatPaginatorIntl, useClass: PersonalizeMatPaginatorIntl}
  ]
})
export class SharedModule { }
