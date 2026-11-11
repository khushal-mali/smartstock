import { IsArray, IsInt, IsNotEmpty, IsNumber, Min, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';

export class PurchaseItemDto {
  @IsInt()
  @Type(() => Number)
  productId: number;

  @IsInt()
  @Min(1, { message: 'Quantity must be at least 1' })
  @Type(() => Number)
  quantity: number;

  @IsNumber({ maxDecimalPlaces: 2 })
  @Min(0)
  @Type(() => Number)
  costPrice: number;
}

export class CreatePurchaseDto {
  @IsInt()
  @Type(() => Number)
  supplierId: number;

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => PurchaseItemDto)
  items: PurchaseItemDto[];
}

