// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ExportBPBlueprintFunctionLibrary.generated.h"

/**
 * 
 */
UCLASS()
class PYAUTOMATION_API UExportBPBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "ExportBP")
	static void GetComponentsFromBlueprintAsset(const UBlueprint* Blueprint,
	TArray<UPrimitiveComponent*>& OutComponents, const FName ComponentTag = "Export");

	UFUNCTION(BlueprintCallable, Category = "ExportBP")
	static void MergeActorToStaticMesh(const FString& InBasePackageName,
		const TArray<UPrimitiveComponent*>& ComponentsToMerge, TArray<UObject*>& AssetsRef);
};
